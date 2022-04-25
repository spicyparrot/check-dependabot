# Python Container Action Template

[![Integration Test](https://github.com/spicyparrot/check-dependabot/actions/workflows/integration.yml/badge.svg?branch=trunk)](https://github.com/spicyparrot/check-dependabot/actions/workflows/integration.yml)
[![Lint](https://github.com/spicyparrot/check-dependabot/actions/workflows/python.yml/badge.svg)](https://github.com/spicyparrot/check-dependabot/actions/workflows/python.yml)

This is a template for creating GitHub actions and contains a small Python application which will be built into a minimal [Container Action](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/creating-a-docker-container-action). Our final container from this template is ~50MB, yours may be a little bigger once you add some code. If you want something smaller check out my [go-container-action template](https://github.com/jacobtomlinson/go-container-action/actions).

In `main.py` you will find a small example of accessing Action inputs and returning Action outputs. For more information on communicating with the workflow see the [development tools for GitHub Actions](https://help.github.com/en/actions/automating-your-workflow-with-github-actions/development-tools-for-github-actions).

> 🏁 To get started, click the `Use this template` button on this repository [which will create a new repository based on this template](https://github.blog/2019-06-06-generate-new-repositories-with-repository-templates/).

Full article here - <https://jacobtomlinson.dev/posts/2019/creating-github-actions-in-python/>

## Requirments

- GitHub Personal Access Token secret

## Usage

This is a simple python action that use the GitHub GraphQL API to check how many open Dependabot alerts are present on the current repository.

This can be used to block merges/deployments if there are outstanding vulnerabilites.

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
        uses: spicyparrot/check-dependabot@v1            
        with:
          github_personal_token: ${{ secrets.ACTIONS_ACCESS_TOKEN }}  

      - name: Check Open Alerts
        run: |
          test "${{ steps.alerts.outputs.total_alerts }}" == "0"
      
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