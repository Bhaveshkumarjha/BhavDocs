from . import db
from datetime import datetime


class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_blocked = db.Column(db.Boolean, default=False)
    allow_undefined_uploads = db.Column(db.Boolean, default=False)

    users = db.relationship("User", backref="company", lazy=True)
    files = db.relationship("File", backref="company", lazy=True)
    folders = db.relationship("Folder", backref="company", lazy=True)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200))
    role = db.Column(db.String(20))
    company_id = db.Column(db.Integer, db.ForeignKey("company.id"))


class Folder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

    company_id = db.Column(
        db.Integer,
        db.ForeignKey("company.id"),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    # Parent folder support
    parent_id = db.Column(
        db.Integer,
        db.ForeignKey("folder.id"),
        nullable=True
    )

    # Subfolders relationship
    subfolders = db.relationship(
        "Folder",
        backref=db.backref("parent", remote_side=[id]),
        lazy="dynamic"
    )

    # Files inside folder
    files = db.relationship(
        "File",
        backref="folder",
        lazy=True
    )


class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    filename = db.Column(
        db.String(200),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="remaining"
    )

    uploaded_at = db.Column(
        db.DateTime,
        nullable=True
    )

    company_id = db.Column(
        db.Integer,
        db.ForeignKey("company.id")
    )

    folder_id = db.Column(
        db.Integer,
        db.ForeignKey("folder.id")
    )

    is_user_upload = db.Column(
        db.Boolean,
        default=False
    )