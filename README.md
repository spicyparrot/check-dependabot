# Check for Dependabot Vulnerability Alerts

[![Integration Test](https://github.com/spicyparrot/check-dependabot/actions/workflows/integration.yml/badge.svg?branch=trunk)](https://github.com/spicyparrot/check-dependabot/actions/workflows/integration.yml)
[![Lint](https://github.com/spicyparrot/check-dependabot/actions/workflows/python.yml/badge.svg)](https://github.com/spicyparrot/check-dependabot/actions/workflows/python.yml)

This is a simple python action that uses the [GitHub GraphQL API](https://docs.github.com/en/graphql/reference/objects#repositoryvulnerabilityalert) to check how many open Dependabot vulnerability alerts are present on a repository.

This can be used to block merges/deployments if there are any outstanding vulnerabilities that need to be resolved first.

## Requirements

- GitHub personal access token that has permissions to view vulnerability alerts of a repo. A guide on how to create one can be found [here](https://docs.github.com/en/enterprise-server@3.4/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- GitHub secret containing your access token.

## Example workflow

```yaml
name: 🚀 Deploy to Prod
on: workflow_dispatch
jobs:
  deploy:
    runs-on: ubuntu-latest
    name: Deployment
    steps:
      - name: Check Dependabot Alerts
        id: alerts
        uses: spicyparrot/check-dependabot@v1.2.0
        with:
          github_personal_token: ${{ secrets.ACTIONS_ACCESS_TOKEN }}  

      - name: Error Exit
        if: steps.alerts.outputs.total_alerts > 0
        run: echo "::error ::Open Vulnerability Alerts Found" && exit 1
      
      - name: Deploy
        run: |
          printf "No open vulnerabilities found. Running deployment now..."
```

### Inputs

| Input                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `github_personal_token`  | A GitHub Access token with access to vulnerability alerts    |

### Outputs

| Output                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `total_alerts`  | The total number of open alerts for your repository    |
| `critical_alerts`  | Number of open critical alerts    |
| `high_alerts`  | Number of open high alerts    |
| `moderate_alerts`  | Number of open moderate alerts   |
| `low_alerts`  | Number of open low alerts    |

### GitHub Summary

Utilizing GitHub [job summaries](https://docs.github.com/en/actions/using-workflows/workflow-commands-for-github-actions#adding-a-job-summary), a table with the breakdown of alerts is now visible as part of the action summary section:

![summary](docs/screenshots/github_summary.png)