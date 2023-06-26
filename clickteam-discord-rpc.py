# File: clickteam-discord-rpc.py
# Project: clickteam-discord-RPC
# File Created: Saturday, ‎Monday, ‎June ‎26, ‎2023, ‏‎9:03:14 AM
# Author: Dooji (doojisbasement@gmail.com)
# GitHub: https://github.com/dooji2
# Discord: dooji_

# Last Modified: ‎Monday, ‎June ‎26, ‎2023, ‏‎12:37:01 PM
# Modified By: Dooji (doojisbasement@gmail.com)

# Copyright (c) 2023 Dooji
import time
import os
import pygetwindow as gw
from pypresence import Presence
from pypresence.exceptions import DiscordNotFound
import threading
import asyncio
import sysconfig
import tempfile
import pkg_resources
import tkinter as tk
from PIL import Image, ImageTk
from pystray import MenuItem as item
import pystray

client_id = "1122799602035339314"

def get_active_project_info():
    try:
        fusion_window = None
        for window in gw.getAllWindows():
            if "Clickteam Fusion" in window.title:
                fusion_window = window
                break

        if fusion_window is None:
            return None, None, None

        window_title_parts = fusion_window.title.split(" - ")
        project_name = window_title_parts[1].split("[")[-1].split("]")[0].strip()

        if len(window_title_parts) > 2:
            frame_name = window_title_parts[-1].rstrip("]")
        else:
            frame_name = None

        return project_name, frame_name, fusion_window.title
    except IndexError:
        return None, None, None

def show_about_dialog(icon, item):
    about_window = tk.Tk()
    about_window.title("About Clickteam Fusion RPC")
    about_window.geometry("300x200")
    about_window.resizable(False, False)

    icon_image = Image.open("dooji.png")
    icon_image = icon_image.resize((100, 100))
    icon_photo = ImageTk.PhotoImage(icon_image)
    icon_label = tk.Label(about_window, image=icon_photo)
    icon_label.image = icon_photo
    icon_label.pack(pady=20)

    credits_label = tk.Label(about_window, text="Author: Dooji\nVersion: 1.0.0\nhttps://github.com/dooji2/clickteam-fusion-rpc/")
    credits_label.pack()

    about_window.eval('tk::PlaceWindow . center')

    about_window.mainloop()


def create_system_tray_icon():
    icon_path = "clickteamrpc.png"
    menu = (item('About', show_about_dialog), item('Exit', lambda: os._exit(0)))
    icon = pystray.Icon("ClickteamRPC", Image.open(icon_path), "Clickteam RPC", menu)
    return icon


def update_presence():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    while True:
        try:
            rpc = Presence(client_id)
            rpc.connect()

            while True:
                try:
                    project_name, frame_name, window_title = get_active_project_info()

                    if project_name:
                        start_time = int(time.time())

                        if frame_name is None:
                            rpc.update(
                                details=f"Project: {project_name}",
                                state="Frame: ",
                                start=start_time,
                                large_image="clickteam",
                                large_text="Clickteam Fusion"
                            )
                        else:
                            if "Clickteam Fusion Developer 2.5+" in window_title:
                                large_image_key = "clickteam"
                            elif "Clickteam Fusion Developer 2.5" in window_title:
                                large_image_key = "clickteam"
                            elif "Clickteam Fusion 2.5+" in window_title:
                                large_image_key = "clickteam_legacy"
                            else:
                                large_image_key = "clickteam"

                            rpc.update(
                                details=f"Project: {project_name}",
                                state=f"Frame: {frame_name}",
                                start=start_time,
                                large_image=large_image_key,
                                large_text="Clickteam Fusion"
                            )
                    else:
                        rpc.clear()

                except Exception:
                    rpc.close()
                    time.sleep(5)
                    continue

                time.sleep(15)
        except DiscordNotFound:
            time.sleep(5)

def main():
    tray_icon = create_system_tray_icon()
    threading.Thread(target=update_presence).start()
    tray_icon.run()

if __name__ == "__main__":
    main()
