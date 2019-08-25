# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import firebase_admin
from firebase_admin import auth, firestore
# [START gae_python37_auth_verify_token]
from flask import Flask, render_template, request, session
from google.auth.transport import requests
from google.cloud import exceptions
from Uploads import upload_file_helper
from models.Posts import Post,Comment
from views.LoginView import security, user_required
from views.SearchImageView import searchImage

firebase_request_adapter = requests.Request()
# Use the application default credentials
options ={
    'serviceAccountId':'shopfinder-247721@appspot.gserviceaccount.com'
}
firebase_admin.initialize_app(options=options)

db = firestore.client()

app = Flask(__name__)
app.register_blueprint(security)
app.register_blueprint(searchImage)
app.secret_key = """Xyeo\x06\x97\xc7\xf7\x1c\x84\xcd\x04\x1e\x07`]\x1fA\x83-\x1e#\xeb@"""
app.config['SESSION_TYPE'] = 'filesystem'


@app.route('/',methods=['GET','POST'])
@user_required
def root():
	if request.method == 'GET':
		all_user_posts = db.collection('Posts').where('uid','==',session['user_id']).get()
		user_record = auth.get_user(session['user_id'])
		params = {
			"first_name"    : user_record.display_name,
			"all_posts"     : all_user_posts,
			"user_image_url": user_record.photo_url,
			"user"          : user_record
		}
		for post in all_user_posts:
			collection = post.collection('Comments')
			print(collection)
		return render_template(
			'home.html',**params)
	elif request.method == 'POST':
		user_record = auth.get_user(session['user_id'])
		if request.files['PostImage'] is not None:
			tags = [request.form['tag1'],request.form['tag2'],request.form['tag3']]
			uploaded_file = request.files['PostImage']
			photo_url = upload_file_helper(uploaded_file)
			post = Post(image_url=photo_url,uid=session['user_id'],username=user_record.display_name,tags=tags)
			db.collection('Posts').add(post.to_dict())
			all_user_posts = db.collection('Posts').where('uid',
			                                              '==',
			                                              session[
				                                              'user_id']).stream()
			template_vars = {
				"all_posts"     : all_user_posts,
				"first_name": user_record.display_name,
				"user_image_url": user_record.photo_url,
				"user"          : user_record
			}
			return render_template("home.html", **template_vars)
		else:
			all_user_posts = db.collection('Posts').where('uid',
			                                              '==',
			                                              session[
				                                              'user_id']).stream()

			template_vars = {
				"all_posts"     : all_user_posts,
				"first_name"    : user_record.display_name,
				"user_image_url": user_record.photo_url ,
				"user"          : user_record
			}
			for post in all_user_posts:
				print(post)
			return render_template("home.html",**template_vars)
# @app.route('/Comment',methods=['POST'])
# @user_required
# def CommentPost():
# 	comment_content = request.form['comment']
# 	post_id = request.form['post']
# 	post_ref = db.collection('Posts').document(post_id)
# 	try:
# 		post = post_ref.get()
# 	except exceptions.NotFound:
# 		print('No such document!')
# 	user_record = auth.get_user(session['user_id'])
# 	comment = Comment(username=user_record.display_name,uid=session['user_id'],content=comment_content)
# 	db.collection





if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.

    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='localhost', port=8080, debug=True)
