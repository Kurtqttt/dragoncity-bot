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
folder_location = 'league_auto_combat_bot/'
window_name = "League Auto Combat Bot"
game_location = "League Battle"
image_hint = "League Text"

# For terminal printing only
GREEN = '\033[92m'
RED = '\033[91m'
RESET = '\033[0m'

# Set uniform values here
uniform_delay = 0.5
uniform_confidence = 0.8

def locate_and_click(image_path, success_message, click=True, delay_execution=0, move_duration=0.66, click_duration=0.01):
    try:
        position = pyautogui.locateOnScreen(image_path, confidence=uniform_confidence)
        if position is not None:
            print(GREEN + f"Found {success_message} at: {position}" + RESET)
            if click:
                time.sleep(delay_execution)
                pyautogui.moveTo(position, duration=move_duration)
                pyautogui.click(position, duration=click_duration)
            return True
    except pyautogui.ImageNotFoundException:
        print(RED + f"Could not locate the {image_path} on the screen." + RESET)
    except Exception as e:
        print(RED + f"An unexpected error occurred: {e}" + RESET)

def show_dialog(message):
    ctypes.windll.user32.MessageBoxW(0, message, "Bot Notification", 1)

# Bot sequence of tasks
def ad_bot_cycle():
    while True:
        if locate_and_click(folder_location + 'next-fight-5h.png', "Next Fight In 5h found", click=False):
            show_dialog("Time to take a break! Next In 6 hours.")
            show_options_dialog()
            break
        elif locate_and_click(folder_location + 'out-of-ads.png', "Out of Ads found", click=False):
            show_dialog("No Ads this time, try again later.")
            show_options_dialog()
            break
        elif locate_and_click(folder_location + 'close-reward.png', 'Close Reward Button found', delay_execution=5):
            continue
        elif locate_and_click(folder_location + 'last-chance.png', 'Last Chance! Text found', click=False):
            locate_and_click(folder_location + 'watch-trailer.png', 'Watch Trailer Button found')
            continue

        tasks = [
            (folder_location + 'opponent.png', 'Opponent found'),
            (folder_location + 'auto-combat-play-button.png', 'Auto Combat Play Button found'),
            (folder_location + 'play-ad.png', 'Play Ad Button found'),
            (folder_location + 'gem-claim.png', 'Gem Claim Button found'),
        ]
        for task in tasks:
            locate_and_click(*task)

def no_ad_bot_cycle():
    while True:
        if locate_and_click(folder_location + 'next-fight-5h.png', "Next In Fight 5h found", click=False):
            show_dialog("Time to take a break! Next In 6 hours.")
            show_options_dialog()
            break
        elif locate_and_click(folder_location + 'last-chance.png', 'Last Chance! Text found', click=False):
            locate_and_click(folder_location + 'close-button.png', 'Close Button found')
            continue
        tasks = [
            (folder_location + 'opponent.png', 'Opponent found'),
            (folder_location + 'auto-combat-play-button.png', 'Auto Combat Play Button found'),
            (folder_location + 'claim.png', 'Claim Button found'),
            (folder_location + 'gem-claim.png', 'Gem Claim Button found'),
        ]
        for task in tasks:
            locate_and_click(*task)

# Step 1: Open a Dialogue
root = tk.Tk()
root.withdraw()

confirmation = messagebox.askquestion(window_name, "Open " + game_location + " and make sure it's in MAXIMIZE window mode. "
                                                        "Ensure it's the FRONTEST program currently running and not blocked by any other program. \n\nHave you followed everything?")

root.destroy()

if confirmation == 'no':
    show_options_dialog()
    sys.exit()

# Step 2: Attempt to locate 
while confirmation == 'yes':
    try:
        position = pyautogui.locateOnScreen(folder_location + 'leagues-text.png', confidence=0.8)
        if position is not None:
            print(GREEN + f"{image_hint} is found at: {position}" + RESET)
            ad_confirmation = messagebox.askquestion('Watch Ads Confirmation', "Do you want to watch ads after every victory?")
            while ad_confirmation == 'yes':
                ad_bot_cycle()
                break
            while ad_confirmation != 'yes':
                no_ad_bot_cycle()
                break
    except pyautogui.ImageNotFoundException:
        print(RED + f"Could not locate {image_hint}." + RESET)
        answer = messagebox.askyesno(window_name, "Are you sure " + game_location + " is open?\n\n"
                                                        "Open " + game_location + " and make sure it's in MAXIMIZE window mode. "
                                                        "Ensure it's the FRONTEST program currently running and not blocked by any other program.\n\n"
                                                        "Would you like to try scanning again?")
        if not answer:
            show_options_dialog()
            break
        else:
            print(f"Searching for the {image_hint}...")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")