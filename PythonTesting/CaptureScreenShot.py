import tkinter as tk
from tkinter import messagebox
import pyautogui
import numpy as np
import serial
import threading
import time

#TIP user rgb color for red: 131,29,25

class TriggerBotApp:
    def __init__(self, master):
        self.master = master
        master.title("Trigger Bot Control")

        self.running = False

        # Color settings
        self.label = tk.Label(master, text="Color Detection (RGB):")
        self.label.pack()

        self.red_entry = tk.Entry(master)
        self.red_entry.insert(0, "0")  # Default value
        self.red_entry.pack()

        self.green_entry = tk.Entry(master)
        self.green_entry.insert(0, "255")  # Default value
        self.green_entry.pack()

        self.blue_entry = tk.Entry(master)
        self.blue_entry.insert(0, "0")  # Default value
        self.blue_entry.pack()

        # Detection status label
        self.detection_status_label = tk.Label(master, text="Detection Status: No Enemy Detected", fg="red")
        self.detection_status_label.pack()

        # Start/Stop button
        self.start_button = tk.Button(master, text="Start", command=self.start_trigger_bot)
        self.start_button.pack()

        self.stop_button = tk.Button(master, text="Stop", command=self.stop_trigger_bot)
        self.stop_button.pack()

        # Status label
        self.status_label = tk.Label(master, text="Status: Stopped")
        self.status_label.pack()

        #TODO implement me
        # Serial setup (example)
        #self.ser = serial.Serial('COM3', 115200)  # Adjust to your port
        time.sleep(2)  # Allow time for connection

    def start_trigger_bot(self):
        if not self.running:
            self.running = True
            self.status_label.config(text="Status: Running")
            threading.Thread(target=self.run_bot).start()  # Run in a separate thread

    def stop_trigger_bot(self):
        self.running = False
        self.status_label.config(text="Status: Stopped")
        self.detection_status_label.config(text="Detection Status: No Enemy Detected", fg="red")  # Reset status

    def run_bot(self):
        while self.running:
            screenshot = pyautogui.screenshot()
            screenshot_np = np.array(screenshot)

            # Get RGB values from entry fields
            red = int(self.red_entry.get())
            green = int(self.green_entry.get())
            blue = int(self.blue_entry.get())
            color_lower = np.array([red - 10, green - 10, blue - 10])
            color_upper = np.array([red + 10, green + 10, blue + 10])

            mask = np.all(np.logical_and(screenshot_np >= color_lower, screenshot_np <= color_upper), axis=-1)
            coordinates = np.argwhere(mask)

            if coordinates.size > 0:
                first_coord = coordinates[0]
                #TODO implement me
                #self.ser.write(f"{first_coord[0]},{first_coord[1]}\n".encode('utf-8'))
                
                # Update detection status
                self.detection_status_label.config(text="Detection Status: Enemy Detected!", fg="green")
            else:
                # Update detection status if no enemy is detected
                self.detection_status_label.config(text="Detection Status: No Enemy Detected", fg="red")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x300")
    app = TriggerBotApp(root)
    root.mainloop()
