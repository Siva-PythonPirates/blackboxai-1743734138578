from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, login_manager

class User(UserMixin, db.Document):
    username = db.StringField(required=True, unique=True)
    email = db.StringField(required=True, unique=True)
    password_hash = db.StringField(required=True)
    role = db.StringField(required=True, choices=[
        'admin', 'coordinator', 'mentor', 'student'
    ])
    profile_pic = db.StringField()
    department = db.StringField()
    batch = db.StringField()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Project(db.Document):
    title = db.StringField(required=True)
    description = db.StringField()
    status = db.StringField(default='unassigned', choices=[
        'unassigned', 'assigned', 'completed'
    ])
    coordinator = db.ReferenceField('User')
    mentor = db.ReferenceField('User')
    github_link = db.StringField()
    paper_link = db.StringField()
    report_link = db.StringField()

class Team(db.Document):
    name = db.StringField(required=True)
    members = db.ListField(db.ReferenceField('User'))
    project = db.ReferenceField('Project')

@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()