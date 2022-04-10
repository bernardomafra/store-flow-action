from .db import db
from datetime import datetime

class Step(db.Document):
    key = db.StringField(required=True)
    key_type = db.StringField(required=True)
    step = db.StringField(required=True)
    action = db.DictField(required=True)


class Flow(db.Document):
    id = db.StringField(primary_key=True)
    website = db.StringField()
    steps = db.ReferenceField(Step, reverse_delete_rule=db.CASCADE)
    status = db.StringField()
    created_at = db.DateTimeField(default=datetime.now())
    updated_at = db.DateTimeField(default=datetime.now())
    finished_at = db.DateTimeField()
    search = db.StringField()
    enabled = db.BooleanField(default=True)
