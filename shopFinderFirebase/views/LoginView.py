from flask import Flask, render_template, redirect, url_for, request,\
	Response,jsonify,session,Blueprint
import flask
from firebase_admin import auth
from Uploads import upload_file_helper
security = Blueprint('security', __name__)

def user_required(handler):
	"""
	Decorator that checks if there's a user associated with the current session.
	Will also fail if there's no session present.
	"""
	def check_login(*args,**kwargs):
		if session.get('user_id') == None:
			return flask.redirect('/login')
		else:
			return handler(*args,**kwargs);
	return check_login

@security.route('/sign_up',methods = ['GET','POST'])
def signup():
	if request.method == 'POST':
		check = request
		password = request.form['password']
		username = request.form['username']
		uploaded_file = request.files['UserImage']
		email = request.form['email']
		photo_url = upload_file_helper(uploaded_file)
		try:
			user_record = auth.create_user(display_name=username,
			                               password=password,email=email,photo_url=photo_url)
		except (ValueError,auth.AuthError) as error:
			params ={
				"bad_login": True,
				"bad_response": str(error)
			}
			return render_template("signup.html")
		try:
			custom_token = auth.create_custom_token(user_record.uid).decode()
			result = {
				'TAG_SUCCESS' : 1,
				'USER_ID': user_record.uid,
				'CUSTOM_TOKEN': custom_token
			}
		except:
			result = {
				'TAG_SUCCESS' : 0,
				'USER_ID': None,
				'CUSTOM_TOKEN': '0'
			}
		return jsonify(result)
	else:
		return render_template("signup.html")

@security.route('/add_user_session',methods = ['POST'])
def add_session():
	try:
		session['user_id'] = request.form['user_id']
		print(session['user_id'])
		session.modified = True
		result ={
			'TAG_SUCCESS': 0
		}
		return jsonify(result)
	except KeyError as error:
		flask.abort(400,str(error))


@security.route('/login',methods = ['POST', 'GET'])
def login():
	if request.method == 'POST':
		email = request.form['email']
		try:
			user_record = auth.get_user_by_email(email)
			result = {
				'TAG_SUCCESS': 1,
				'USER_ID': user_record.uid,
			}
		except (ValueError, auth.AuthError) as error:
			result = {
				'TAG_SUCCESS': 0,
				'bad_response': str(error)
			}
		return jsonify(result)
	else:
		return render_template("login.html")

@security.route('/logout',methods=['GET'])
def logout():
	session.pop('user_id',None)
	return flask.redirect('/login')