from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, ValidationError, pre_load
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)


class Book(db.Model):
	__tablename__ = "books"
	id = db.Column(db.Integer, primary_key=True)
	topic = db.Column(db.Text, nullable=True)
	title = db.Column(db.Text, nullable=False)
	scholar_name = db.Column(db.Text, nullable=True)
	link = db.Column(db.Text, nullable=False)

	def __repr__(self):
		return '<Books %r>' % self.title

class Dars(db.Model):
	__tablename__ = "deroos"
	id = db.Column(db.Integer, primary_key=True)
	is_active = db.Column(db.Boolean, nullable=False)
	topic = db.Column(db.Text, nullable=True)
	title = db.Column(db.Text, nullable=False)
	location = db.Column(db.Text, nullable=False)
	am_pm = db.Column(db.Text, nullable=False)
	start_time = db.Column(db.Text, nullable=False)
	end_time = db.Column(db.Text, nullable=False)
	date = db.Column(db.Date, nullable=False)
	weekly_or_monthly_or_daily = db.Column(db.Text, nullable=True)
	scholar_name = db.Column(db.Text, db.ForeignKey('scholars.scholar_name'), nullable=False)
	scholars = db.relationship('Scholar', backref=db.backref('deroos', lazy=True))

	def __repr__(self):
		return '<Dars %r>' % self.title

class Scholar(db.Model):
	__tablename__ = "scholars"
	scholar_name = db.Column(db.Text, primary_key=True)
	creation_time = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp(), nullable=False)
	sex = db.Column(db.CHAR, nullable=True)
	email = db.Column(db.Text, nullable=False)
	website = db.Column(db.Text, nullable=False)
	photo_url = db.Column(db.Text, nullable=False)
	bio = db.Column(db.Text, nullable=True)

	def __repr__(self):
		return '<Scholar %r>' % self.scholar_name

class BookSchema(Schema):
	id = fields.Int(dump_only=True)
	topic = fields.String()
	title = fields.String()
	scholar_name = fields.String()
	link = fields.String()

	
class DarsSchema(Schema):
	id = fields.Int(dump_only=True)
	is_active = fields.Bool()
	topic = fields.String()
	title = fields.String()
	location = fields.String()
	am_pm = fields.String()
	start_time = fields.String()
	end_time = fields.String()
	date = fields.Date()
	weekly_or_monthly_or_daily = fields.String()
	scholar_name = fields.String()

class ScholarSchema(Schema):
	scholar_name = fields.String()
	creation_time = fields.DateTime()
	sex = fields.String()
	email = fields.String()
	website = fields.String()
	photo_url = fields.String()
	bio = fields.String()
