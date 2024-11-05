import os
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def init_db(app):
    # Environment-based database configuration
    if os.getenv("FLASK_ENV") == "production":
        app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://oliviajain:SqlPassword@oliviajain.mysql.pythonanywhere-services.com/oliviajain$default'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///local.db'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

# Define the User and Answer models


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # Track which question the user is on
    current_question = db.Column(db.Integer, default=0)
    answers = db.relationship('Answer', backref='user', lazy=True)


class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
