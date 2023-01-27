from flask import Flask
from dotenv import load_dotenv
import os
from download_script import *

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/<script>")
def run_script(script):
    load_dotenv()
    srnd = randomstr(7)
    new_script = srnd + "_" + script
    scriptpath = os.environ["gcs_script_folder"] + "/" + script
    destinationfile = "/tmp/" + new_script 
    download_script_from_gcs(os.environ["gcp_project"], scriptpath, destinationfile )
    print("Downloaded script at " + destinationfile)

    print("Run " + destinationfile)
    os.system("chmod u+x " + destinationfile)
    os.system(destinationfile)
    os.system("rm " + destinationfile)


    return { "result": True, "message": script + " has finished." }

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=8080)