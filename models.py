from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.orm import relationship


db = SQLAlchemy()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    date_joined = db.Column(db.Date, default=datetime.utcnow)

    def __repr__(self):
        return f"<User: {self.username}>"
    

class Map(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    html = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    date_created = db.Column(db.Date, default=datetime.utcnow)

    user = relationship("User")

    def __repr__(self):
        return f"<Map: {self.id}>"