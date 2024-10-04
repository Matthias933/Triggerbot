import board
import busio
import time
import usb_hid
from adafruit_hid.mouse import Mouse
import digitalio
import usb_cdc

led = digitalio.DigitalInOut(board.LED)
led.direction = digitalio.Direction.OUTPUT

# Create a Mouse object
mouse = Mouse(usb_hid.devices) 

while True:
    if usb_cdc.console.in_waiting > 0:
        # Read the incoming message
        coords = usb_cdc.console.read(usb_cdc.console.in_waiting).decode("utf-8").strip()
        
        if coords: 
            #rpi pi receives an x and y value which is the distance to the enemy
            x, y, rotate_mouse = map(int, coords.split(','))
            
            if rotate_mouse != 0:
               mouse.move(rotate_mouse, 0) #only moving mouse on X axcis
            else:
                # Move to coords
                mouse.move(x, y)
                mouse.click(Mouse.LEFT_BUTTON)
                led.value = True
            
    else:
        #mouse.move(100, 0)  # Move the mouse right when no coordinates are received
        led.value = False
