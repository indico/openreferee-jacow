from .db import db


class Event(db.Model):
    __tablename__ = "events"
    identifier = db.Column(db.String, primary_key=True)
    title = db.Column(db.String, nullable=False)
    url = db.Column(db.String, nullable=False)
    token = db.Column(db.String, nullable=False)
    endpoints = db.Column(db.JSON, nullable=False)
