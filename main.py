# Querying GitHub API for open Dependabot Alerts #####
import os
import requests
import pandas as pd


# Functions
def get_header(token):
    auth="Bearer " + token
    authdict={"Authorization": auth}
    return authdict

# A simple function to use requests.post to make the API call. Note the json= section.
def run_query(query,token): 
    head=get_header(token)
    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=head)
    if request.status_code == 200:
        response=request.json()
        return response
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))

def get_alerts(repo,owner,token): #  A simple function to use requests.post to make the API call. Note the json= section.
    # The GraphQL query (with a few aditional bits included) itself defined as a multi-line string.       
    query = """
    {
        repository(name: "spicyparrot", owner: "spicyparrot-backend") {
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
    result=run_query(query,token)
    # Flatten into a dataframe
    rows=result['data']['repository']['vulnerabilityAlerts']['nodes']
    alerts=pd.json_normalize(rows)

    # Return the number of alerts to console
    return alerts

def main():
    # Get inputs from envars (GitHub converts all inputs into INPUT_<UPPER CASE OF INPUT>)
    token = os.environ["INPUT_GITHUB_TOKEN"]
    owner = os.environ["GITHUB_REPOSITORY_OWNER"]
    repo = os.environ["GITHUB_REPOSITORY"]
    repo = repo.split("/")[-1]                      #  Cleans the in-case we get 'owner/repo' format
    # Query GitHub for full alerts breakdown
    alerts=get_alerts(repo,owner,token)
    # Meta data
    totalAlerts=len(alerts)
    #TODO - severe vs critical etc 
    #Set Outputs
    print(f"::set-output name=total_alerts::{totalAlerts}")


if __name__ == "__main__":
    main()


