"""
	Entry point for flask app controlling /files endpoint
	TODO: add a firebase config service? so we're not copy pasting all this stuff into every endpoint
		  figure out better auth flow...
		  setup trace route, debugging, logging, centralized documentation (can we publish to a wiki or something?)
"""
from flask import Flask, redirect, url_for, request, render_template, jsonify
import requests
from flask_cors import CORS, cross_origin
import pyrebase

app = Flask(__name__)
CORS(app)

# Set up database connection.
config = {
    'apiKey': "AIzaSyDpFoAzfFzzcCmYkMwkAz61wUY_O5z9KM4", 
    'authDomain': "cloudide-3d6ca.firebaseapp.com", 
    'databaseURL': "https://cloudide-3d6ca.firebaseio.com", 
    'projectId': "cloudide-3d6ca", 
    'storageBucket': "cloudide-3d6ca.appspot.com", 
    'messagingSenderId': "42881595105"
}

firebase = pyrebase.initialize_app(config)

# Set up the user
auth = firebase.auth()
user = auth.sign_in_with_email_and_password('jmankhan1@gmail.com', 'password')

db = firebase.database()

@app.route("/files")
def getFile():
	"""
		Gets file content by id, if provided
		Gets list of files by project id, if provided
		Params are matched in order, i.e. project_id is ignored if id is provided
		TODO: better error handling
	"""
	id = request.args.get('id')
	project_id = request.args.get('project_id');
	file = ''
	if(id != None):
		file = db.child('files').child(id).get(user['idToken'])
	elif(project_id != None):
		file = db.child('files').order_by('project_id').equal_to(project_id).get(user['idToken'])
	else:
		return 'error'

	return jsonify(file.val())

@app.route("/files/", methods=["POST"])
def insertFile():
	"""
		Inserts a new file 
		Use the following curl command to test:
		curl -X POST -H "Content-Type: application/json" -d '{"id" : "5", "content" : "Jalal is the best ever", "project_id" : "4"}' http://localhost:5000/files/

		TODO: better error handling!
	"""
	data = request.get_json()

	try:
		db.child("files").push(data, user['idToken'])
	except:
		return "Something went wrong inserting the file"
	
	return "Success"

if __name__ == "__main__":
	app.run(host='0.0.0.0', debug=True)

