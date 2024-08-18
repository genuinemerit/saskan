import os
import sys
import app_saskan

#!/usr/bin/env python


def main():
    # Set up the environment
    # ...

    # Launch the app_saskan.py module
    try:
        app_saskan.main()
    except ImportError:
        print("Error: app_saskan module not found.")
        sys.exit(1)


if __name__ == "__main__":
    main()