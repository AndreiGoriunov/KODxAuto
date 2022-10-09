from lib.kodxauto import KODxAuto


def run(file_path):
    kodxauto = KODxAuto(file_path)
    kodxauto.start()
    kodxauto.print_attrs()
