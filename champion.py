import time

import pytesseract
import cv2
import numpy as np
from PIL import Image, ImageGrab
from matplotlib import pyplot as plt
from phue import Bridge

bridge_ip = '192.168.0.10'

b = Bridge(bridge_ip)
b.get_api()

x = 645
y = 575
x_offset = 1220
y_offser = 180
replacements = (('1', 'l'), ('0', 'o'))

names = [i for i in b.get_light_objects('name')]
lights = b.get_light_objects('name')

original_hue = []
og_sat = []
for i, light in enumerate(names):
    original_hue.append(lights[light].hue)
    og_sat.append(lights[light].saturation)

while True:
    img = ImageGrab.grab(bbox=(x, y, x + x_offset, y + y_offser)).convert('L')
    img = np.array(img)

    img = cv2.GaussianBlur(img, (5, 5), 0)
    img = cv2.threshold(img, 120, 255, cv2.THRESH_BINARY)[1]
    cv2.imshow('window', img)
    
    text = pytesseract.image_to_string(img).replace(" ", "").lower()

    for old, new in replacements:
        text = text.replace(old, new)
        
    if text is not "":
        print(text)
        
    if "champion" in text:
        print("Winner winner")
        for i, light in enumerate(names):
            lights[light].saturation = 255
            lights[light].hue = 27000
        cv2.waitKey(15000)

        for i, light in enumerate(names):
            lights[light].saturation = og_sat[i]
            lights[light].hue = original_hue[i]
        
    if "ameove" in text:
        print("loser")
        for i, light in enumerate(names):
            lights[light].saturation = 255
            lights[light].hue = 0
        cv2.waitKey(15000)

        for i, light in enumerate(names):
            lights[light].saturation = og_sat[i]
            lights[light].hue = original_hue[i]
        
    if cv2.waitKey(250) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

