import pyautogui
import time

print("Move your mouse to the desired position. You have 5 seconds...")
time.sleep(5)

position = pyautogui.position()
print(f"Current mouse position is: {position}")
