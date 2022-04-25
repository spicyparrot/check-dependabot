#https://gist.github.com/gbaman/b3137e18c739e0cf98539bf4ec4366ad
#token = "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"

#########################################################
#### Querying GitHub API for open Dependabot Alerts #####
#########################################################

import requests
import sys
import json
import pprint as pp
import pandas as pd

# Parse CLI arguments
owner = sys.argv[1]
repo = sys.argv[2]
token = sys.argv[3]

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

# Run queries
result=runQuery(query,token)

# Flatten into a dataframe
rows=result['data']['repository']['vulnerabilityAlerts']['nodes']
flat=pd.json_normalize(rows)
alerts=len(flat)

# Return the number of alerts to console
print(str(alerts))