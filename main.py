# Querying GitHub API for open Dependabot Alerts #####
import os
import requests
import sys
import json
import pprint as pp
import pandas as pd

# GitHub converts all inputs into INPUT_<UPPER CASE OF INPUT>
def main():
    my_input = os.environ["INPUT_MYINPUT"]

    my_output = f"Hello {my_input}"
    total_alerts = "10"

    print(f"::set-output name=myOutput::{my_output}")
    print(f"::set-output name=total_alerts::{total_alerts}")


if __name__ == "__main__":
    main()
