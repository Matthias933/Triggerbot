import pyautogui
from PIL import Image
import numpy as np
import time

def find_enemypos_in_screenshot():
    screenshot = pyautogui.screenshot()

    # Convert the screenshot to a NumPy array
    screenshot_np = np.array(screenshot)

    # Current color detection is only for red highlicht color
    green_lower = np.array([175, 38, 58])
    green_upper = np.array([206, 86, 95])

    green_mask = np.all(np.logical_and(screenshot_np >= green_lower, screenshot_np <= green_upper), axis=-1)

    green_coordinates = np.argwhere(green_mask)

    return [(x, y) for y, x in green_coordinates]

while True:
    coordinates = find_enemypos_in_screenshot()
    if coordinates:
        print("enemy detected.")
        
        first_coord = coordinates[0] 
        print(f"Cordinates are: {first_coord}")

        #TODO remove me rpi will handle this to simulate a real mouse
        pyautogui.moveTo(first_coord[0], first_coord[1], duration=0.1) 

        time.sleep(1);
    else:
        print("No enemy detected.")
    