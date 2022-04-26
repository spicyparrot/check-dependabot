# Check for Dependabot Vulnerability Alerts

[![Integration Test](https://github.com/spicyparrot/check-dependabot/actions/workflows/integration.yml/badge.svg?branch=trunk)](https://github.com/spicyparrot/check-dependabot/actions/workflows/integration.yml)
[![Lint](https://github.com/spicyparrot/check-dependabot/actions/workflows/python.yml/badge.svg)](https://github.com/spicyparrot/check-dependabot/actions/workflows/python.yml)

This is a simple python action that uses the GitHub GraphQL API to check how many open Dependabot alerts are present on the current repository.

This can be used to block merges/deployments if there are any outstanding vulnerabilites that need to be resolved first.

## Requirments

- A GitHub personal access token that has permissions to view vulnerability alerts of a repo

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
        uses: spicyparrot/check-dependabot@trunk
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

## Future Work

- Breakdown of alerts by severity (e.g. number of critical issues)
- Investigation into using `GITHUB_TOKEN` instead of a personal access token
- Paginate all results (currently limited to first 100 alerts which means `total_alerts` is not 100% accurate if a repo has more than 100 open alerts)
- Better error logging for unauthorised token