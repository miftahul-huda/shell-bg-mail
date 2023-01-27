# shell-bg-mail

## About

This is a python program to run a unix shell script stored in Google Cloud Storage. This includes python programs to run BigQuery jobs and send email using smtp. 

## Usage

**To use the mail program:**

_python mail.py -t "$recepient" -s "$subject" -b "$emailbody"

**To use the BQ program:**

_python3 bq.py -q "$query"_

**To run the server:**

_python server.py_

**To call the server to run a shell script :**

_http://localhost:5050/{scriptfilename}_

## Configuration

To configure the server, bigquery job and the mail program, open the .env file and set these values:

*   _smtp\_server_, the smtp server to send email from
*   _smtp\_port_, the smtp port to send email from
*   _smtp\_user_, the user to send the email from
*   _smtp\_password_, the password for the smtp user. This password must be base64 encoded.
*   _gcp\_project_, the GCP project where the BigQuery and Cloud Storage resides.
*   _gcs\_script\_folder_, the folder in Google Cloud Storage where the script file is stored.
