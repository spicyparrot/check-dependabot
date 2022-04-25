import os
import requests  # noqa We are just importing this to prove the dependency installed correctly


def main():
    my_input = os.environ["INPUT_MYINPUT"]    #GitHub converts all inputs into INPUT_<UPPER CASE OF INPUT>

    my_output = f"Hello {my_input}"

    print(f"::set-output name=myOutput::{my_output}")


if __name__ == "__main__":
    main()
