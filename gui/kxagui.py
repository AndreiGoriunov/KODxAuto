import os
from tkinter import ttk
import tkinter as tk

from kodxauto import KODxAuto


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

        macros_list = self.__get_macros_list()
        macro_select_combobox = ttk.Combobox(root, state="readonly", values=macros_list)
        macro_select_combobox.set(self.kxa.get_property("macro_name"))
        macro_select_combobox.grid(row=1, column=2)

        self.run_macro_btn = tk.Button(
            root,
            text="Run",
            width=10,
            height=1,
            command=lambda: self.run_macro(macro_select_combobox.get()),
        )
        self.run_macro_btn.grid(row=1, column=1)

        self.execution_progress_label = tk.Label(root, text="Not Running")
        self.execution_progress_label.grid(row=1,column=3)

        return root

    def render(self):
        self.root.mainloop()
    
    def run_macro(self, macro_name):
        # Update window when the Run button is pressed
        self.execution_progress_label.configure(text="Running")
        self.run_macro_btn.configure(state="disabled")
        self.root.update()
        # Calling run() method of KODxAuto instance
        status = self.kxa.run(macro_name)
        # Updating window when run() method concluded
        self.execution_progress_label.configure(text=f"Finished: {status}")
        self.run_macro_btn.configure(state="active")
        self.root.update()

    def __get_macros_list(self):
        # Set the directory you want to list
        macros_directory = self.kxa.get_property("macros_directory")
        # Get the list of all folders in directory
        macro_names = [
            f
            for f in os.listdir(macros_directory)
            if os.path.isdir(os.path.join(macros_directory, f))
        ]
        return macro_names
