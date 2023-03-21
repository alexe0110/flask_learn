from sqlalchemy import MetaData, Table, Integer, String, TIMESTAMP, ForeignKey, Column, DateTime

metadata= MetaData()

Articles = Table(
    "Articles",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String, nullable=False),
    Column("intro", String, nullable=False),
    Column("text", String, nullable=False),
    Column("date", DateTime, nullable=False),
)


# from flask import Flask, render_template, url_for, request, redirect
# from flask_sqlalchemy import SQLAlchemy
# from datetime import datetime

# app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///blog.db"
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# db = SQLAlchemy(app)


# class Articles(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(100), nullable=False)
#     intro = db.Column(db.String(300), nullable=False)
#     text = db.Column(db.Text, nullable=False)
#     date = db.Column(db.DateTime, default=datetime.utcnow)

#     def __repr__(self):
#         return '<Article %r>' % self.id
