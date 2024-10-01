import tkinter as tk
from tkinter import messagebox
import pyautogui
import numpy as np
import serial
import threading
import time

# TIP: User RGB color for red: 131,29,25

class TriggerBotApp:

    ser = serial.Serial('COM5', 9600)

    def __init__(self, master):
        self.master = master
        master.title("Trigger Bot Control")
        master.configure(bg = "#222831")

        self.running = False

        # Color settings
        self.label = tk.Label(master, text="Color Detection (RGB):", fg="#EEEEEE", bg="#222831")
        self.label.pack()

        self.red_entry = tk.Entry(master, fg="#EEEEEE", bg="#222831")
        self.red_entry.insert(0, "131")  # Default value for red
        self.red_entry.pack()

        self.green_entry = tk.Entry(master, fg="#EEEEEE", bg="#222831")
        self.green_entry.insert(0, "29")  # Default value for green
        self.green_entry.pack()

        self.blue_entry = tk.Entry(master, fg="#EEEEEE", bg="#222831")
        self.blue_entry.insert(0, "25")  # Default value for blue
        self.blue_entry.pack()

        # Detection status label
        self.detection_status_label = tk.Label(master, text="Detection Status: No Enemy Detected", fg="red", bg="#222831")
        self.detection_status_label.pack()

        # Start/Stop button
        self.start_button = tk.Button(master, text="Start", command=self.start_trigger_bot, fg="#EEEEEE", bg="#00ADB5")
        self.start_button.pack()

        self.stop_button = tk.Button(master, text="Stop", command=self.stop_trigger_bot, fg="#EEEEEE", bg="#00ADB5")
        self.stop_button.pack()

        # Status label
        self.status_label = tk.Label(master, text="Status: Stopped", fg="#EEEEEE", bg="#222831")
        self.status_label.pack()

        time.sleep(2)  # Allow time for serial connection

    def start_trigger_bot(self):
        if not self.running:
            self.running = True
            self.status_label.config(text="Status: Running")
            threading.Thread(target=self.run_bot).start()  # Run in a separate thread

    def stop_trigger_bot(self):
        self.running = False
        self.status_label.config(text="Status: Stopped")
        self.detection_status_label.config(text="Detection Status: No Enemy Detected", fg="red", bg="#222831")  # Reset status

    def run_bot(self):
        screen_width, screen_height = pyautogui.size()
        print(screen_width, screen_height)
        center_x = screen_width // 2
        center_y = screen_height // 2
        region_size = 25  # Size of the region around the center to check for color

        while self.running:
            screenshot = pyautogui.screenshot(region=(center_x - region_size, center_y - region_size, region_size * 2, region_size * 2))
            screenshot_np = np.array(screenshot)

            # Get RGB values from entry fields
            red = int(self.red_entry.get())
            green = int(self.green_entry.get())
            blue = int(self.blue_entry.get())
            color_lower = np.array([red - 10, green - 10, blue - 10])
            color_upper = np.array([red + 10, green + 10, blue + 10])

            # Check if the specified color is within the region around the center
            mask = np.all(np.logical_and(screenshot_np >= color_lower, screenshot_np <= color_upper), axis=-1)
            if np.any(mask):
                # If the color is found, trigger the bot
                print("Enemy detected in center region!")
                self.ser.write(b"1\n")
                self.detection_status_label.config(text="Detection Status: Enemy Detected!", fg="green", bg="#222831")
            else:
                self.ser.write(b"0\n")
                print("No Enemy detected in center region!")
                self.detection_status_label.config(text="Detection Status: No Enemy Detected", fg="red", bg="#222831")

            time.sleep(0.5)  # Adjust frequency of checking

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x300")
    app = TriggerBotApp(root)
    root.mainloop()
