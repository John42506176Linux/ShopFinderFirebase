from google.cloud import storage
import io
from PIL import Image
# Instantiates a client


GCS_BUCKET = 'shopfinderprimebucket'  # enter the name of your bucket
#Params:FileStorge Object

def upload_file_helper(uploaded_file):
	gcs = storage.Client()

	# Get the bucket that the file will be uploaded to.
	bucket = gcs.get_bucket(GCS_BUCKET)

	# Create a new blob and upload the file's content.
	blob = bucket.blob(uploaded_file.filename)

	blob.upload_from_string(
		uploaded_file.read(),
		content_type=uploaded_file.content_type
	)

	# The public URL can be used to directly access the uploaded file
	# via HTTP.
	return blob.public_url

def upload_user_photo(user_photo):
	gcs = storage.Client()

	# Get the bucket that the file will be uploaded to.
	bucket = gcs.get_bucket(GCS_BUCKET)
	img_bytes = io.BytesIO(user_photo.read())
	img = Image.open(img_bytes)

	# Create a new blob and upload the file's content.
	blob = bucket.blob(user_photo.filename)

	blob.upload_from_string(
		img.resize(32, 32).tobytes(),
		content_type=user_photo.content_type
	)

	# The public URL can be used to directly access the uploaded file
	# via HTTP.
	return blob.public_url