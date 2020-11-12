from . import __version__


SERVICE_INFO = {"version": __version__, "name": "OpenReferee JACoW"}
DEFAULT_TAGS = {
    "TC01": {"title": "Incorrect title, authors affiliation formatting", "color": "red", "system": False},
    "TC02": {"title": "Text formatting incorrect (paragraphs, section...)", "color": "blue", "system": False},
    "TC03": {"title": "Table formatting incorrect (not centered, outside of margins...)",
             "color": "orange", "system": False},
    "TC04": {"title": "Figure formatting incorrect (caption missing, outside of margins...)",
             "color": "purple", "system": False},
    "PRC": {"title": "Processed", "color": "brown", "system": True},
    "QA01": {"title": "QA Approved", "color": "green", "system": True},
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
            "extensions": ["tex", "doc", "docx"],
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
