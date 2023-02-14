import sys, getopt
import argparse
from dotenv import load_dotenv
import os
from google.cloud import storage
import datetime


def main():

    load_dotenv()

    parser = argparse.ArgumentParser(
                    prog = 'upload2gcs',
                    description = 'Upload file to gcs',
                    epilog = 'Devoteam')

    parser.add_argument('-f', '--file', help='The file to be uploaded', required=True)
    parser.add_argument('-p', '--path', help='The GCS path where file is uploaded', required=True)  
    args = parser.parse_args()


    now = datetime.datetime.now()
    upload(args.file, args.path)
    
def strip_end(text, suffix):
    if suffix and text.endswith(suffix):
        return text[:-len(suffix)]
    return text

def upload(file, gcspath):

    gcspath = strip_end(gcspath, "/")
    client = storage.Client( project=os.environ['gcp_project'])
    gcspath = gcspath.replace('gs://', "")
    mybucket = gcspath.split("/")[0]
    myfile = gcspath.replace(mybucket, "") 
    if(len(myfile) > 0 and myfile[0] == "/"):
        myfile = myfile[1:len(myfile)]
   
    if(len(myfile) > 0):
        myfile += "/" + os.path.basename(file)
    else:
        myfile += os.path.basename(file)

    print("upload " + file + " to gs://" + mybucket + "/" + myfile)

    bucket = client.get_bucket(mybucket)
    blob = bucket.blob(myfile)
    blob.upload_from_filename(file)
    print("upload done")

if __name__ == "__main__":
    main()



