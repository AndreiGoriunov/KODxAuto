import kodxauto
from gui.kxagui import KXAGUI


def main():
    kxa = kodxauto.KODxAuto()
    kxagui = KXAGUI(kxa)
    kxagui.render()


if __name__ == "__main__":
    main()
