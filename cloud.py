import os
from google.cloud import storage

# Imports the Google Cloud client library
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "googlecloud_bookkey.json"
# Instantiates a client
storage_client = storage.Client()

# book-thing is our bucket name
my_bucket = storage_client.get_bucket("book-thing")


def upload_to_bucket(blob_name, file_path):
    try:
        bucket = storage_client.get_bucket(my_bucket)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(file_path)
        return True
    except Exception as e:
        print(e)
        return False

# example: uploading a image from my pc
# path = r'C:\Users\ハオやん\Desktop\movie'
print(os.getcwd())
path_parent = os.path.dirname(os.getcwd())
os.chdir(path_parent)
print(os.getcwd())
upload_to_bucket("logo1", os.path.join(os.getcwd(), "logo.png"))


def download_file_from_bucket(blob_name, file_path):
    try:
        bucket = storage_client.get_bucket(my_bucket)
        blob = bucket.blob(blob_name)
        with open(file_path, "wb") as f:
            storage_client.download_blob_to_file(blob, f)
        return True
    except Exception as e:
        print(e)
        return False

# download_file_from_bucket("logo", os.path.join(os.getcwd(), "logo.png"))
# file_path we got our current directory from os.getcwd(), name the file into "logo.png"