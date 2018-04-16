#coding:utf8
from flask import Flask, render_template
from flask_restful import Resource, Api, abort
from models import db, app, Dars, Scholar, ScholarSchema, DarsSchema
from flask import jsonify
from sqlalchemy.exc import IntegrityError

api = Api(app)
scholars_schema = ScholarSchema(many=True)
scholar_schema = ScholarSchema()
deroos_schema = DarsSchema(many=True)
dars_schema = DarsSchema()

@app.route('/')
def home():
	return render_template('index.html')

	  # return 'zakeeha API v1.0 - This is an attempt to collect information around available/active\n'\
	  # 'islamic sessions/seminars and serve them in a RESTful API available for consumption by anyone for free.\n\n'\
	  # 'The following is a list of available GET endpoints (so far):\n'\
	  # '- /all_deroos (returns all available lists of deroos whether active or not\n'\
	  # '- /active_deroos (returns a list of active deroos only\n'\
	  # '- /inactive_deroos (return a list of inactive deroos only\n'\
	  # '- /scholar_names (retruns a list of names for all available scholars\n'\
	  # '- /all_deroos/<scholar_name> returns a list of all deroos by scholar_name'

class all_deroos(Resource):
	def get(self):
		deroos = Dars.query.all()
		result = deroos_schema.dump(deroos)
		return jsonify({'deroos': result.data.encode('utf-8')})

class active_deroos(Resource):
	def get(self):
		active_deroos = Dars.query.filter(Dars.is_active.is_(True)).all()
		result = deroos_schema.dump(active_deroos)
		return jsonify({'active_deroos': result.data})

class inactive_deroos(Resource):
	def get(self):
		inactive_deroos = Dars.query.filter(Dars.is_active.is_(False)).all()
		result = deroos_schema.dump(inactive_deroos)
		return jsonify({'inactive_deroos': result.data})

class all_scholars(Resource):
	def get(self):
		scholars = Scholar.query.all()
		result = scholars_schema.dump(scholars)
		return jsonify({'scholars': result.data})

class deroos_by_scholar_name(Resource):
	def get(self, scholar_name):
		if Scholar.query.filter(Scholar.scholar_name == scholar_name).count() > 0:
			deroos_by_scholar_name = Dars.query.filter(Dars.scholar_name == scholar_name)
			result = deroos_schema.dump(deroos_by_scholar_name)
			return jsonify({'deroos': result.data})
		else:
			return jsonify({"message": "Scholar could not be found."})
		


#api.add_resource(welcome, '/')
api.add_resource(all_deroos, '/all_deroos')
api.add_resource(active_deroos, '/active_deroos')
api.add_resource(inactive_deroos, '/inactive_deroos')
api.add_resource(all_scholars, '/all_scholars')
api.add_resource(deroos_by_scholar_name, '/all_deroos/<scholar_name>')


if __name__ == '__main__':
	app.run(debug=True)