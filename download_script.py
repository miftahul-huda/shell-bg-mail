from google.cloud import storage
import string
import random


def randomstr(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def download_script_from_gcs(gcs_project, gcs_file_path, destination_file_name):
    # Initialise a client
    storage_client = storage.Client(gcs_project)

    ppath = gcs_file_path.split("/")
    bucket_name = ppath[0]

    gcs_file_path = gcs_file_path.replace(bucket_name + "/", "")

    #print(bucket_name)
    #print(gcs_file_path)
    # Create a bucket object for our bucket
    bucket = storage_client.get_bucket(bucket_name)
    # Create a blob object from the filepath
    blob = bucket.blob(gcs_file_path)
    # Download the file to a destination
    blob.download_to_filename(destination_file_name)