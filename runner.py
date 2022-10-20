import os
from sys import argv, exit
import logging
from src import kodxauto

DIRNAME = os.path.dirname(os.path.abspath(__file__))


def main():
    if len(argv) < 2:
        print(
            """Usage:
        - argv[1]: name of the feature file (macros file)
        - **argv:  additional behave arguments
        """
        )
        exit()

    logging.basicConfig(
        filename=os.path.join(DIRNAME, "run.log"),
        filemode="w",
        level=logging.INFO,
        encoding="utf-8",
        format="%(asctime)s [%(levelname)s]: %(message)s",
        datefmt="%H:%M:%S",
    )

    args = [arg for arg in argv[2:]]

    logging.info("in runner")

    kxa = kodxauto.KODXAuto(DIRNAME)
    kxa.set_macros_name(argv[1])
    kxa.set_args(args)
    kxa.run()


if __name__ == "__main__":
    main()
