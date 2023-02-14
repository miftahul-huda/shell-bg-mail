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

    job_config = bigquery.QueryJobConfig(
        # Run at batch priority, which won't count toward concurrent rate limit.
        priority=bigquery.QueryPriority.BATCH
    )


    try:
        results = client.query(q, job_config)  # Make an API request.
        #listed_jobs = client.list_tables(max_results=10)
        rows = results.result()  # Waits for query to finish 
        fields  = results._query_results._properties['schema']['fields']

        #print(listed_jobs)
        #for job in listed_jobs:
        #    print(job)
        fieldnames = ""
        for field in fields:
            fieldnames += field['name'] + "\t|"

        if(len(fieldnames) > 0):
            fieldnames = fieldnames[0:len(fieldnames) -1]
        print (fieldnames)

        rowline = ""
        for row in rows:
            # Row values can be accessed by field name or index.
            for f in fields:
                rowline += str(row[f['name']]) + "\t"                    
            print(rowline)
            rowline = ""
    except:
        print("error")
        if(results.errors != None):
            print(results.errors)


    print("---bq.py Run BQ srcipt done")

if __name__ == "__main__":
    main()



