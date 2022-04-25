import os
import requests  # noqa We are just importing this to prove the dependency installed correctly


def main():
    my_input = os.environ["INPUT_MYINPUT"]

    my_output = f"Hello {my_input}"
    total_alerts = "10"

    print(f"::set-output name=myOutput::{my_output}")
    print(f"::set-output name=total_alerts::{total_alerts}")


if __name__ == "__main__":
    main()
