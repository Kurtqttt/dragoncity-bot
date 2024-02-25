import tkinter as tk
from tkinter import simpledialog
import subprocess
import os

options = ["Watch DTV Ads", "Watch Greenhouse Ads", "Collect All Gold"]

class OptionDialog(simpledialog.Dialog):
    def __init__(self, parent, title, options, execute_func):
        self.options = options
        self.execute_func = execute_func
        self.dialog_closed = False  
        super().__init__(parent, title)

    def body(self, master):
        tk.Label(master, text="Master, ask me what to do. You can choose from the options below.").pack()

        self.var = tk.StringVar(master)
        self.var.set(self.options[0])  # Set the default option

        option_menu = tk.OptionMenu(master, self.var, *self.options)
        option_menu.pack()

    def apply(self):
        selected_option = self.var.get()
        if selected_option:
            self.execute_func(selected_option)
        else:
            self.dialog_closed = True

def show_options_dialog():
    root = tk.Tk()
    root.withdraw()

    dlg = OptionDialog(root, "Dragon City Bot", options, execute_selected_option)
    result = dlg.result

    if dlg.dialog_closed:
        print("Options dialog closed thus closing the program.")
    else:
        print("Options dialog canceled thus closing the program.")

    return result

def execute_selected_option(selected_option):
    if selected_option == "Watch DTV Ads":  
        print("Selected: Watch DTV Ads")
        script_path = os.path.join(os.path.dirname(__file__), "watch_dtv_ad_bot", "watch_dtv_ad_bot.py")
        subprocess.run(["python", script_path])
    elif selected_option == "Watch Greenhouse Ads":  
        print("Selected: Watch Greenhouse Ads")
        script_path = os.path.join(os.path.dirname(__file__), "watch_greenhouse_ad_bot", "watch_greenhouse_ad_bot.py")
        subprocess.run(["python", script_path])
    else:
        print("Unknown option:", selected_option)