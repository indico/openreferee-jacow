import os
import tempfile
from collections import defaultdict

import requests
from flask import current_app

from . import ghostscript
from .defaults import (
    ACTION_ROLES,
    CUSTOM_ACTIONS,
    DEFAULT_EDITABLES,
    DEFAULT_FILE_TYPES,
    DEFAULT_TAGS,
    PUBLISH_AFTER_QA,
    Tag,
)


def setup_requests_session(token):
    session = requests.Session()
    session.headers = {"Authorization": "Bearer {}".format(token)}
    if current_app.debug:
        session.verify = False
    return session


def get_event_tags(session, event):
    tag_endpoint = event.endpoints["tags"]["list"]

    current_app.logger.info("Fetching available tags...")
    response = session.get(tag_endpoint)
    response.raise_for_status()
    return {t["code"]: t for t in response.json()}


def setup_event_tags(session, event):
    tag_endpoint = event.endpoints["tags"]["create"]
    available_tags = get_event_tags(session, event)

    current_app.logger.info("Adding missing tags...")
    for code, data in DEFAULT_TAGS.items():
        if code in available_tags:
            # tag already available in Indico event
            continue
        response = session.post(tag_endpoint, json=dict(data, code=code))
        response.raise_for_status()
        current_app.logger.info("Added '{}'...".format(code))


def cleanup_event_tags(session, event):
    available_tags = get_event_tags(session, event)
    for tag_name in DEFAULT_TAGS:
        if tag_name not in available_tags:
            continue
        tag = available_tags[tag_name]
        if not tag["is_used_in_revision"]:
            # delete tag, as it's unused
            response = session.delete(tag["url"])
            response.raise_for_status()
            current_app.logger.info("Deleted tag '{}'".format(tag["title"]))


def get_file_types(session, event, editable):
    endpoint = event.endpoints["file_types"][editable]["list"]
    current_app.logger.info("Fetching available file types ({})...".format(editable))
    response = session.get(endpoint)
    response.raise_for_status()
    return {t["name"]: t for t in response.json()}


def setup_file_types(session, event):
    for editable in DEFAULT_EDITABLES:
        available_file_types = get_file_types(session, event, editable)
        for type_data in DEFAULT_FILE_TYPES[editable]:
            if type_data["name"] in available_file_types:
                continue
            endpoint = event.endpoints["file_types"][editable]["create"]
            response = session.post(endpoint, json=type_data)
            response.raise_for_status()
            current_app.logger.info(
                "Added '{}' to '{}'".format(type_data["name"], type_data)
            )


def cleanup_file_types(session, event):
    for editable in DEFAULT_EDITABLES:
        available_types = get_file_types(session, event, editable)
        for ftype in DEFAULT_FILE_TYPES[editable]:
            server_type = available_types[ftype["name"]]
            if not server_type["is_used_in_condition"] and not server_type["is_used"]:
                response = session.delete(server_type["url"])
                response.raise_for_status()
                current_app.logger.info(
                    "Deleted file type '{}'".format(server_type["name"])
                )


def cleanup_event(event):
    session = setup_requests_session(event.token)
    cleanup_event_tags(session, event)
    cleanup_file_types(session, event)


def process_editable_files(session, files, upload_endpoint):
    uploaded = defaultdict(list)
    for file in files:
        if os.path.splitext(file["filename"])[1] != ".pdf":
            uploaded[file["file_type"]].append(file["uuid"])
            continue
        upload = process_pdf(file, session, upload_endpoint)
        uploaded[file["file_type"]].append(upload["uuid"])

    return uploaded


def replace_revision(session, event, files, replace_endpoint):
    available_tags = get_event_tags(session, event)
    response = session.post(
        replace_endpoint,
        json={
            "files": files,
            "state": "ready_for_review",
            "comment": "The PDFs in this review have been distilled.",
            "tags": [available_tags[Tag.PROCESSED]["id"]],
        },
    )
    response.raise_for_status()


def process_pdf(file, session, upload_endpoint):
    _dir = os.path.dirname(__file__)
    with (
        tempfile.NamedTemporaryFile() as out_file,
        tempfile.NamedTemporaryFile() as in_file,
    ):
        resp = session.get(file["signed_download_url"])
        in_file.write(resp.content)
        in_file.seek(0)
        args = [
            "-dBATCH",
            "-dNOPAUSE",
            "-dSAFER",
            "-dFIXEDMEDIA",
            "-dDEVICEWIDTHPOINTS=595",
            "-dDEVICEHEIGHTPOINTS=792",
            "-sDEVICE=pdfwrite",
            "-r1200",
            "-dCompatibilityLevel=1.6",
            "-dPDFSETTINGS=/prepress",
            "-dSubsetFonts=true",
            "-dCompressFonts=false",
            "-dEmbedAllFonts=true",
            "-dNOPLATFONTS",
            "-I " + os.path.join(_dir, "gsfonts"),
            "-sFONTPATH=" + os.path.join(_dir, "gsfonts"),
            "-sOutputFile=" + out_file.name,
            in_file.name,
        ]
        ghostscript.run_file(args)
        r = session.post(
            upload_endpoint,
            files={"file": (file["filename"], out_file, file["content_type"])},
        )
        return r.json()


def process_accepted_revision(event, revision):
    session = setup_requests_session(event.token)
    available_tags = get_event_tags(session, event)
    revision_tags = [t["id"] for t in revision["tags"]]
    return dict(
        publish=False,
        tags=revision_tags + [available_tags[Tag.QA_PENDING]["id"]],
    )


def _can_access_action(revision, action, user):
    if not any(x["code"] in ACTION_ROLES for x in user["roles"]):
        return False
    if revision["final_state"]["name"] == "accepted":
        if any(t["code"] == Tag.QA_PENDING for t in revision["tags"]):
            return action in ("approve-qa", "fail-qa")
        return action == "fail-qa"
    return False


def get_custom_actions(event, revision, user):
    return [a for a in CUSTOM_ACTIONS if _can_access_action(revision, a["name"], user)]


def process_custom_action(event, revision, action, user, endpoints):
    if not _can_access_action(revision, action, user):
        return {}
    session = setup_requests_session(event.token)
    available_tags = get_event_tags(session, event)
    revision_tags = [
        t["id"]
        for t in revision["tags"]
        if t["id"]
        not in [
            available_tags[Tag.QA_APPROVED]["id"],
            available_tags[Tag.QA_PENDING]["id"],
        ]
    ]
    if action == "approve-qa":
        return {
            "tags": revision_tags + [available_tags[Tag.QA_APPROVED]["id"]],
            "publish": PUBLISH_AFTER_QA,
            "comments": [{"internal": True, "text": "This revision has passed QA."}],
        }
    elif action == "fail-qa":
        response = session.post(
            endpoints["revisions"]["reset"],
        )
        response.raise_for_status()
        return {
            "tags": revision_tags,
            "publish": False,
            "comments": [{"internal": True, "text": "This revision has failed QA."}],
        }
    return {}
