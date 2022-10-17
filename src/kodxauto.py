import logging
import os

DIRNAME = os.path.dirname(os.path.abspath(__file__))
STATUSES = {0: "running", 1: "complete", 2: "error"}

logging.basicConfig(
    filename=os.path.join(DIRNAME, "..\\run.log"),
    filemode="w",
    level=logging.DEBUG,
    encoding="utf-8",
    format="%(asctime)s [%(levelname)s]: %(message)s",
    datefmt="%H:%M:%S",
)


def run(dir_name, app_name, **kwargs):
    print(f'Framework Home: {dir_name}\napp_name={app_name},kwargs={kwargs}')
    print(f'behave {dir_name}\\macros\\{app_name}\\features')
    logging.info('Testings')
