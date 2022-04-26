# Querying GitHub API for open Dependabot Alerts #####
import os
import requests
import pandas as pd
import pprint as pp


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
    # TODO - get around the pagination limits for accurate total issues
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
    query=query.replace("REPO_NAME",repo)
    query=query.replace("REPO_OWNER",owner)
    # Query GitHub API
    result=run_query(query,token)
    pp.pprint(result)
    # Flatten into a dataframe
    rows=result['data']['repository']['vulnerabilityAlerts']['nodes']
    rows=pd.json_normalize(rows)
    # Append into an empty state to handle 0 rows
    alerts=pd.DataFrame(columns = ['state','securityVulnerability.severity','createdAt','dismissedAt'])
    alerts = alerts.append(rows)
    alerts=alerts.rename(columns={"securityVulnerability.severity": "severity"})
    # Return the number of alerts to console
    return alerts

def main():
    # Get inputs from envars (GitHub converts all inputs into INPUT_<UPPER CASE OF INPUT>)
    token = os.environ["INPUT_GITHUB_PERSONAL_TOKEN"]
    owner = os.environ["GITHUB_REPOSITORY_OWNER"]
    repo = os.environ["GITHUB_REPOSITORY"]
    repo = repo.split("/")[-1]                      #  Cleans the in-case we get 'owner/repo' format
    # Query GitHub for full alerts breakdown
    alerts=get_alerts(repo,owner,token)
    pp.pprint(alerts)
    # Breakdown stats
    statsDict={"total_alerts": len(alerts)}
    statsDict['critical_alerts']=len(alerts.loc[alerts['severity'] == 'CRITICAL'])
    statsDict['high_alerts']=len(alerts.loc[alerts['severity'] == 'HIGH'])
    statsDict['moderate_alerts']=len(alerts.loc[alerts['severity'] == 'MODERATE'])
    statsDict['low_alerts']=len(alerts.loc[alerts['severity'] == 'LOW'])
    pp.pprint(statsDict)
    #Set Outputs
    print(f"::set-output name=total_alerts::{statsDict['total_alerts']}")
    print(f"::set-output name=critical_alerts::{statsDict['critical_alerts']}")
    print(f"::set-output name=high_alerts::{statsDict['high_alerts']}")
    print(f"::set-output name=moderate_alerts::{statsDict['moderate_alerts']}")
    print(f"::set-output name=low_alerts::{statsDict['low_alerts']}")


if __name__ == "__main__":
    main()


