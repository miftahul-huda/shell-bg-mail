import sys, getopt
import argparse
from dotenv import load_dotenv
import os
from google.cloud import bigquery


def main():

    load_dotenv()

    parser = argparse.ArgumentParser(
                    prog = 'BQ Runner',
                    description = 'Run query against BigQuery',
                    epilog = 'Devoteam')

    parser.add_argument('-q', '--query', help='The query to be executed')  
    args = parser.parse_args()

    print("Running BQ scripts")
    bqrun(args.query)


def bqrun(q):
    # Construct a BigQuery client object.
    client = bigquery.Client(project=os.environ["gcp_project"])

    queries = q.split(";")

    for query in queries:

        if(query != None and len(query.strip()) > 0):
            print ("---bq.py Run query----")
            #print ("-------Query:")
            #print (query)
            results = client.query(query)  # Make an API request.
            rows = results.result()  # Waits for query to finish
            if(results.errors != None):
                print(results.errors)

        #for row in results:
            
    print("---bq.py Run BQ srcipt done")

if __name__ == "__main__":
    main()



