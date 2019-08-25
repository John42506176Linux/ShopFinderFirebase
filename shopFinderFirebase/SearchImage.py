from google.cloud import vision
import io
import json
import requests
# Import the base64 encoding library.
import base64

# Pass the image data to an encoding function.
# def encode_image(image):
# 	image_content = image.read()
# 	return base64.b64encode(image_content)
def detect_web_by_url(url):
	"""Detects web annotations given an image."""

	client = vision.ImageAnnotatorClient()

	image = vision.types.Image(source=url)
	response = client.web_detection(image=image,max_results=5)
	annotations = response.web_detection
	list_of_entity_links = []

	if annotations.web_entities:
		for entity in annotations.web_entities:
			CustomSearchParams = {
			    "key": "AIzaSyAso_n3tH-AGcXaXHBt5YLaHSdV3XoXMvM",
			    "cx" : "006239744188845988923:qyi6wbfdc_g",
			    "q"  : entity.description,
			    "num": 5
			}
			search_query = requests.get(
			    "https://www.googleapis.com/customsearch/v1",
			    params=CustomSearchParams)
			search_dict = json.loads(search_query.text)
			entity_link_list = []
			for search in search_dict['items']:
				entity_link_list.append(
					(entity.description, search['link']))
			list_of_entity_links.append(entity_link_list)
	list_of_guess_links=[]
	if annotations.best_guess_labels:
		for label in annotations.best_guess_labels:
			CustomSearchParams = {
				"key": "AIzaSyAso_n3tH-AGcXaXHBt5YLaHSdV3XoXMvM",
				"cx" : "006239744188845988923:qyi6wbfdc_g",
				"q"  : label.label,
				"num": 5
			}
			search_query = requests.get(
				"https://www.googleapis.com/customsearch/v1",
				params=CustomSearchParams)
			search_dict = json.loads(search_query.text)
			guess_link_list = []
			for search in search_dict['items']:
				guess_link_list.append(
					(label.label, search['link']))
			list_of_guess_links.append(guess_link_list)
	urls =[]
	if annotations.pages_with_matching_images:
		for page in annotations.pages_with_matching_images:
			urls.append(page.url)
	return list_of_entity_links,list_of_guess_links,urls

def detect_web_by_upload_file(file):
	"""Detects web annotations given an image."""

	client = vision.ImageAnnotatorClient()

	image = vision.types.Image(content=file.read())
	response = client.web_detection(image=image,max_results=5)
	print(response)
	annotations = response.web_detection
	list_of_entity_links = []

	if annotations.web_entities:
		for entity in annotations.web_entities:
			CustomSearchParams = {
			    "key": "AIzaSyAso_n3tH-AGcXaXHBt5YLaHSdV3XoXMvM",
			    "cx" : "006239744188845988923:qyi6wbfdc_g",
			    "q"  : entity.description,
			    "num": 5
			}
			search_query = requests.get(
			    "https://www.googleapis.com/customsearch/v1",
			    params=CustomSearchParams)
			search_dict = json.loads(search_query.text)
			entity_link_list = []
			if 'items' in search_dict:
				for search in search_dict['items']:
					entity_link_list.append(
						(entity.description, search['link']))
			list_of_entity_links.append(entity_link_list)
	list_of_guess_links=[]
	if annotations.best_guess_labels:
		for label in annotations.best_guess_labels:
			CustomSearchParams = {
				"key": "AIzaSyAso_n3tH-AGcXaXHBt5YLaHSdV3XoXMvM",
				"cx" : "006239744188845988923:qyi6wbfdc_g",
				"q"  : label.label,
				"num": 5
			}
			search_query = requests.get(
				"https://www.googleapis.com/customsearch/v1",
				params=CustomSearchParams)
			search_dict = json.loads(search_query.text)
			guess_link_list = []
			if 'items' in search_dict:
				for search in search_dict['items']:
					guess_link_list.append(
						(label.label, search['link']))
			list_of_guess_links.append(guess_link_list)
	urls =[]
	if annotations.pages_with_matching_images:
		for page in annotations.pages_with_matching_images:
			urls.append(page.url)
	return list_of_entity_links,list_of_guess_links,urls