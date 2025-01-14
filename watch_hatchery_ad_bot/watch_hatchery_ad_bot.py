import pyautogui
import time
import ctypes
import sys
import os
import tkinter as tk
from tkinter import messagebox

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from options import show_options_dialog

# Variable declarations
folder_location = 'watch_hatchery_ad_bot/'
window_name = "Watch Hatchery Ads Bot"
game_location = "Hatchery"
image_hint = "Hatchery Play Button"

# For terminal printing only
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

# Set uniform values here
uniform_delay = 0.5
uniform_confidence = 0.8

def locate_and_click(image_path, success_message, click=True, delay_execution=0):
    try:
        position = pyautogui.locateOnScreen(image_path, confidence=uniform_confidence)
        if position is not None:
            print(GREEN + f"Found {success_message} at: {position}" + RESET)
            if click:
                time.sleep(delay_execution)
                pyautogui.moveTo(position, duration=0.66)
                pyautogui.click(position, duration=0.01)
            return True
    except pyautogui.ImageNotFoundException:
        print(RED + f"Could not locate the {image_path} on the screen." + RESET)
    except Exception as e:
        print(RED + f"An unexpected error occurred: {e}" + RESET)

def show_dialog(message):
    ctypes.windll.user32.MessageBoxW(0, message, "Bot Notification", 1)

# Bot sequence of tasks
def bot_cycle():
    while True:
        if locate_and_click(folder_location + 'out-of-ads.png', "Out of Ads found", click=False):
                show_dialog("No Ads this time, try again later.")
                show_options_dialog()
                break
        elif locate_and_click(folder_location + 'close-reward.png', 'Close Reward Button found', delay_execution=5):
                continue
        tasks = [
            (folder_location + 'hatchery-open-again.png', 'Hatchery Open Again Button found'),
            (folder_location + 'skip-6h.png', 'Skip 6h Button found'),
            (folder_location + 'close-reward.png', 'Close Reward Button found'),
            (folder_location + 'hatchery-close.png', 'Hatchery Close Button found'),
        ]
        for task in tasks:
            locate_and_click(*task)

# Step 1: Open a Dialogue
root = tk.Tk()
root.withdraw()

confirmation = messagebox.askquestion(window_name, "Locate " + game_location + " and make sure it's in MAXIMIZE window mode. "
                                                        "Ensure it's the FRONTEST program currently running and not blocked by any other program. \n\nHave you followed everything?")

root.destroy()

if confirmation == 'no':
    show_options_dialog()
    sys.exit()

# Step 2: Attempt to locate
while confirmation == 'yes':
    try:
        position = pyautogui.locateOnScreen(folder_location + 'hatchery-play-button.png', confidence=0.8)
        if position is not None:
            print(GREEN + f"{image_hint} is found at: {position}" + RESET)
            pyautogui.click(position)
            bot_cycle()
            break
    except pyautogui.ImageNotFoundException:
        print(RED + f"Could not locate {image_hint}." + RESET)
        answer = messagebox.askyesno(window_name, "Are you sure " + game_location + " is located?\n\n"
                                                        "Locate " + game_location + " and make sure it's in MAXIMIZE window mode. "
                                                        "Ensure it's the FRONTEST program currently running and not blocked by any other program.\n\n"
                                                        "Would you like to try scanning again?")
        if not answer:
            show_options_dialog()
            break
        else:
            print(f"Searching for the {image_hint}...")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")