
import tkinter as tk
from tkinter import messagebox
from playsound import playsound

def alarmpopup(alarm_time):
    root = tk.Tk()
    root.withdraw()  

    try:
        playsound("frontend\\assets\\audio\\alarm.mp3")  
    except Exception as e:
        print("Error playing sound:", e)

    # Show the popup message
    root.destroy()

