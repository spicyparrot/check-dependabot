# Check for Dependabot Vulnerabilty Alerts

[![Integration Test](https://github.com/spicyparrot/check-dependabot/actions/workflows/integration.yml/badge.svg?branch=trunk)](https://github.com/spicyparrot/check-dependabot/actions/workflows/integration.yml)
[![Lint](https://github.com/spicyparrot/check-dependabot/actions/workflows/python.yml/badge.svg)](https://github.com/spicyparrot/check-dependabot/actions/workflows/python.yml)

This is a simple python action that uses the GitHub GraphQL API to check how many open Dependabot alerts are present on the current repository.

This can be used to block merges/deployments if there are any outstanding vulnerabilites that need to be resolved first.

## Requirments

- A GitHub personal access token that has permissions to view vulnerabilty alerts of a repo

## Example workflow

```yaml
name: Deploy to Prod
on: workflow_dispatch
jobs:
  deploy:
    runs-on: ubuntu-latest
    name: Deployment
    steps:
      - name: Check Dependabot Alerts
        id: alerts
        uses: spicyparrot/check-dependabot@trunk        #Check out yourself to test
        with:
          github_personal_token: ${{ secrets.ACTIONS_ACCESS_TOKEN }}  

      - name: View Outputs
        run: |
          export ALERTS=${{ steps.alerts.outputs.total_alerts }}
          if [[ "$ALERTS" > 0 ]] ; then
              echo "::error ::⚠ $ALERTS Open Vulnerabilty Alerts Found" && exit 1
          else
            echo "::debug ::✅ $ALERTS Open Vulnerabilty Alerts Found"
          fi
      
      - name: Deploy
        run: |
          print "No open vulnerabilities found. Running deployment now..."
```

### Inputs

| Input                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `github_personal_token`  | A GitHub Access token with access to vulnerability alerts    |

### Outputs

| Output                                             | Description                                        |
|------------------------------------------------------|-----------------------------------------------|
| `total_alerts`  | The total number of open alerts for your repository    |