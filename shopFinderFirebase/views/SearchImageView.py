from flask import render_template, request,\
	Blueprint
from SearchImage import detect_web_by_upload_file,detect_web_by_url
searchImage = Blueprint('searchImage', __name__)

@searchImage.route('/SearchImage',methods=['POST'])
def SearchImage():
	if 'SearchImage' in request.files:
		(entity_links,guess_links,urls)=\
			detect_web_by_upload_file(
				request.files['SearchImage'])
	elif 'SearchImage' in request.form:
		(entity_links, guess_links, urls) = \
			detect_web_by_url(
			request.files['SearchImage'])
	template_vars = {
		"search_contents": entity_links,
		"urls"           : urls,
		"guess_links"    : guess_links
	}
	return render_template("Image-Search.html", **template_vars)