import os
from sys import argv

from src import kodxauto

DIRNAME = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    if len(argv) < 2:
        print(
            """Usage:
        argv[1]: path to the saved macros folder
        """
        )
    kwargs = dict(arg.split("=") for arg in argv[2:])
    kodxauto.run(DIRNAME, argv[1], **kwargs)
