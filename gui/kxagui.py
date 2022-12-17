from kodxauto import KODxAuto
import tkinter as tk


class KXAGUI:
    def __init__(self, kxa_instance: KODxAuto):
        self.kxa = kxa_instance
        self.root = self.__build_components()

    def __build_components(self):
        root = tk.Tk(className=f"{self.kxa}")
        root.title("KODXAuto")
        root.iconbitmap("gui/resources/KOD.ico")
        root.geometry("300x200")
        root.resizable(False, False)

        run_btn = tk.Button(root, text="Run", width=10, height=1, command=self.kxa.run).grid(
            row=1, column=1
        )
        return root

    def render(self):
        self.root.mainloop()
