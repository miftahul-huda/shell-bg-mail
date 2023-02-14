import sys, getopt
import argparse
from dotenv import load_dotenv
import os
from google.cloud import bigquery
from google.api_core.exceptions import BadRequest
import datetime
import re



def main():

    load_dotenv()

    parser = argparse.ArgumentParser(
                    prog = 'BQ Runner',
                    description = 'Run query against BigQuery',
                    epilog = 'Devoteam')

    parser.add_argument('-q', '--query', help='The query to be executed', required=True)
    parser.add_argument('-s', '--start', help='The start number of query to be executed', required=False)  
    args = parser.parse_args()

    if(args.start == None):
        args.start = 1

    now = datetime.datetime.now()
    print("Start running BQ scripts at " + str(now))
    bqrun(args.query, int(args.start))

    now = datetime.datetime.now()
    print("\n\nFinished running BQ scripts at " + str(now))

def set_declare(query, declares, sets):
    decs = ""
    sets2 = ""
    for declare in declares:
        regex = "declare\s+([A-Za-z0-9_]+)\s+"
        variables = re.findall(regex, declare, re.IGNORECASE)
        if(len(variables) > 0):
            variable = variables[0]
            if(variable in query):
                decs += declare + ";\n"


    for set in sets:
        regex = "set\s+([A-Za-z0-9_]+)\s+"
        variables = re.findall(regex, set, re.IGNORECASE)
        if(len(variables) > 0):
            variable = variables[0]
            if(variable in query):
                sets2 += set + ";\n"

    query = decs + "" + sets2 + "" + query
    return query        

def bqrun(q, start):
    # to store declare and set queries
    declares = []
    sets = []

    # flag to run query. Don't run declare and set query.
    run_query = True

    # Construct a BigQuery client object.
    client = bigquery.Client(project=os.environ["gcp_project"])
    counter = 1
    queries = q.split(";")
    results = ""
    for query in queries:
        run_query = True
        if(query != None and len(query.strip()) > 0):
            if(counter >= start):
                query = query.strip()

                try:

                    if(query.lower().find("declare") == 0):
                        declares.append(query)
                        run_query = False
                    if(query.lower().find("set") == 0):
                        sets.append(query)
                        run_query = False
                    
                    if(run_query):
                       
                        query = set_declare(query, declares, sets)
                        print("======================================================")
                        print("Query #{}:".format(counter))
                        print(query[0:100] + "...")

                        #if(query != None and "select" in query.lower()):
                        #    print("\n======================================================\n" + query + "\n======================================================\n")
                        

                        job_config = bigquery.QueryJobConfig(
                            # Run at batch priority, which won't count toward concurrent rate limit.
                            priority=bigquery.QueryPriority.BATCH
                        )

                        now1 = datetime.datetime.now()
                        results = client.query(query, job_config)  # Make an API request.
                        rows = results.result()  # Waits for query to finish
                        now2 = datetime.datetime.now()

                        t = now2 - now1
                        print("\nQuery is succesful and it took " + str(t) + " to complete.")

                        if("select" in query.lower()):
                            print("The query result:")
                            #print(results._query_results._properties['schema']['fields'])
                            fields  = results._query_results._properties['schema']['fields']
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
                        

                            #print ("---Done bq.py Run query----")
                        print("======================================================")

                except BadRequest as e:
                    print("\n\nQuery Error, Query# {}".format(counter))
                    #print("\n===================Error Query===================================\n")
                    print (query)
                    #print("\n===================/Error Query===================================\n")
                    print("\nQuery error: {}".format(e.args[0]))
                    print("======================================================")
                except KeyboardInterrupt:
                    # quit
                    print("Keyboard interrupt... exiting...")
                    sys.exit()
                except:
                    print("\n\nQuery Error, Query# {}".format(counter))
                    #print("\n===================Error Query===================================\n")
                    print (query)
                    #print("\n===================/Error Query===================================\n")
                    if(results.errors != None):
                        print(results.errors)
                    print("======================================================")
            

            if(run_query): 
                counter = counter + 1



        #for row in results:
            
    print("---bq.py Run BQ srcipt done")

if __name__ == "__main__":
    main()



