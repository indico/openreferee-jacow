from . import __version__


SERVICE_INFO = {"version": __version__, "name": "OpenReferee JACoW"}
DEFAULT_TAGS = {
    "ERR_WRONG_TITLE": {"title": "Wrong Title", "color": "red", "system": False},
    "ERR_SILLY_TITLE": {"title": "Silly Title", "color": "orange", "system": False},
    "OK_TITLE": {"title": "Title OK", "color": "green", "system": False},
    "PROCESSED": {"title": "Processed", "color": "brown", "system": True},
    "QA_APPROVED": {"title": "QA Approved", "color": "green", "system": True},
}
DEFAULT_EDITABLES = {"paper", "poster"}
DEFAULT_FILE_TYPES = {
    "paper": [
        {
            "name": "PDF",
            "extensions": ["pdf"],
            "allow_multiple_files": False,
            "required": True,
            "publishable": True,
            "filename_template": "{code}_paper",
        },
        {
            "name": "Source Files",
            "extensions": ["tex", "doc"],
            "allow_multiple_files": True,
            "required": True,
            "publishable": False,
        },
    ],
    "poster": [
        {
            "name": "PDF",
            "extensions": ["pdf"],
            "allow_multiple_files": False,
            "required": True,
            "publishable": True,
            "filename_template": "{code}_poster",
        },
        {
            "name": "Source Files",
            "extensions": ["ai", "svg"],
            "allow_multiple_files": False,
            "required": True,
            "publishable": False,
        },
    ],
}
ACTION_ROLES = {
    "SCS": {"title": "Scientific Secretary", "color": "blue"}
}
CUSTOM_ACTIONS = [
    {
        "name": "fail-qa",
        "title": "Fail QA",
        "color": "orange",
        "confirm": "Are you sure you want to fail the QA step?",
    },
    {"name": "approve-qa", "title": "Approve QA", "color": "teal", "icon": "check"}
]
