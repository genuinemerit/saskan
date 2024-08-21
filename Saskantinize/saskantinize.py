#!/usr/bin/env python

# import os
import sys

from Saskantinize import app_saskantinize


def main():
    # Set up the environment
    # ...

    # Launch the app_saskan.py module
    try:
        # app_saskantinize.main()
        app_saskantinize.SaskanAdmin()
    except ImportError:
        print("Error: app_saskantinize module not found.")
        sys.exit(1)


# if __name__ == "__main__":
#     main()
