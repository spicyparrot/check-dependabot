# Querying GitHub API for open Dependabot Alerts #####
import os
import requests
import sys
import json
import pprint as pp
import pandas as pd


# Functions
def getHeader(token):
    auth="Bearer " + token
    dict={"Authorization": auth}
    return dict

def runQuery(query,token): # A simple function to use requests.post to make the API call. Note the json= section.
    head=getHeader(token)
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=head)
    if request.status_code == 200:
        response=request.json()
        return response
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

def getAlerts(repo,owner,token): # A simple function to use requests.post to make the API call. Note the json= section.
    # The GraphQL query (with a few aditional bits included) itself defined as a multi-line string.       
    query = """
    {
        repository(name: "REPO_NAME", owner: "REPO_OWNER") {
            vulnerabilityAlerts(first: 100,states: OPEN) {
                nodes {
                    state
                    createdAt
                    dismissedAt
                    state
                    securityVulnerability {
                        severity
                    }
                }
            }
        }
    }
    """
    # Parameterise the name/owner of the repo
    query=query.replace("REPO_OWNER",owner)
    query=query.replace("REPO_NAME",repo)
    # Query GitHub API
    result=runQuery(query,token)
    # Flatten into a dataframe
    rows=result['data']['repository']['vulnerabilityAlerts']['nodes']
    alerts=pd.json_normalize(rows)

    # Return the number of alerts to console
    return alerts

# GitHub converts all inputs into INPUT_<UPPER CASE OF INPUT>
def main():
    # Get inputs from envars
    repo = os.environ["INPUT_REPO"]
    owner = os.environ["INPUT_REPO_OWNER"]
    token = os.environ["INPUT_GITHUB_TOKEN"]
    # Query GitHub for full alerts breakdown
    alerts=getAlerts(repo,owner,token)
    # Meta data
    total_alerts=len(alerts)
    #TODO - severe vs critical etc 
    #Set Outputs
    print(f"::set-output name=total_alerts::{total_alerts}")


if __name__ == "__main__":
    main()


