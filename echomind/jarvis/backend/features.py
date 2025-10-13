import datetime
from pyexpat import model

import re
import struct
import subprocess
import time
import webbrowser

import pvporcupine
import pyaudio 
import pyautogui
import pyjokes
import requests 
from playsound import playsound 
import eel
import os

import google.generativeai as genai

import pygetwindow as gw
import wikipedia
from backend.config import ASSISTANT_NAME
import pywhatkit as kit
import sqlite3

from datetime import datetime
from backend.helper import extract_yt_term, remove_words
from backend.command import speak, takecommand


con = sqlite3.connect("jarvis.db")
cursor = con.cursor()


#playing assistant sound  funtion
@eel.expose
def playAssistantSound():
    music_dir="frontend\\assets\\audio\\sound1.mp3"
    playsound(music_dir)


import webbrowser

def openCommand(query):
    query = query.replace(ASSISTANT_NAME.strip().lower(), "").replace("open", "").strip().lower()

    if "search" in query:
        try:
            parts = query.split("search")
            search_text = parts[1].strip()  # text after "search"
            search_query = search_text.replace(" ", "+")
            google_url = f"https://www.google.com/search?q={search_query}"

            speak(f"Searching for {search_text} on Google")
            webbrowser.open(google_url)
        except Exception as e:
            speak("Something went wrong while trying to search.")
            rs=0
            msg="Something went wrong while trying to search."
            eel.receiverText(msg, rs)
            print(e)

    else:
        try:
            if " Word" in query:
                speak("Opening Microsoft Word")
                os.startfile("winword")
                return

            elif "powerpoint" in query or "power point" in query:
                speak("Opening PowerPoint")
                rs=0.4
                msg=" PowerPoint opened"
                eel.receiverText(msg, rs)
                os.startfile("powerpnt")
                return
            # Try to open app from system commands DB
            cursor.execute("SELECT path FROM sys_command WHERE name = ?", (query,))
            result = cursor.fetchone()
            if result:
                speak(f"Opening {query}")
                os.startfile(result[0])
                return

            # Try to open website from DB
            cursor.execute("SELECT url FROM web_command WHERE name = ?", (query,))
            result = cursor.fetchone()
            if result:
                speak(f"Opening {query}")
                webbrowser.open(result[0])
                return
            speak(f" opening {query}")
            os.system('start ' + query)
            
            
        except Exception as e:
            speak("Something went wrong.")
            rs=0
            msg="Something went wrong."
            eel.receiverText(msg, rs)
            print(e)

   
           
def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("playing "+search_term+" on YouTube")
    kit.playonyt(search_term)
    msg="played on youtube"
    rs=11
    eel.receiverText(msg, rs)
    
def hotword():
    porcupine = None
    paud = None
    audio_stream = None
    try:
        # Access key for Picovoice
        access_key = "PwhxPmAJUfXRS3YT1lNhS65u4qZtzjvyzhhenboiZ1Y60eACU+m/Jw=="  
        
        # Path to the custom "echo mind" model file
        jarvis_path = r"C:\Users\91830\Downloads\Echo-Mind_en_windows_v3_0_0\Echo-Mind_en_windows_v3_0_0.ppn"

        # Create Porcupine instance
        porcupine = pvporcupine.create(
            access_key=access_key,
            keyword_paths=[jarvis_path]  
        )
        

        # Initialize audio stream
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )

        # Hotword detection loop
        while True:
            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)

            # Process the audio data
            keyword_index = porcupine.process(keyword)

            # Hotword detected
            if keyword_index >= 0:
                print("Hotword detected: echo mind")

                # Press the Win + J shortcut key using pyautogui
                pyautogui.keyDown("win")
                pyautogui.press("j")
                time.sleep(2)
                pyautogui.keyUp("win")
                
    except Exception as e:
        print(f"Error occurred: {e}")
        rs=0
        msg=f"Error occurred: {e}"
        eel.receiverText(msg, rs)

    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()
        print("Resources cleaned up")
        
# Contact finder
def findContact(query):
    words_to_remove = [ASSISTANT_NAME, 'make', 'a', 'to', 'voice', 'call', 'send', 'message', 'whatsapp', 'video']
    query = remove_words(query, words_to_remove)

    try:
        query = query.strip().lower()
        cursor.execute(
            "SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?",
            ('%' + query + '%', query + '%')
        )
        results = cursor.fetchall()
        print("Contact found:", results[0][0])
        mobile_number_str = str(results[0][0])
        if not mobile_number_str.startswith('+91'):
            mobile_number_str = '+91' + mobile_number_str
        return mobile_number_str, query
    except Exception as e:
        speak('Contact not found.')
        print("DB Error:", e)
        return 0, 0

# WhatsApp automation
def whatsApp(mobile_no, message, flag, name):
    try:
        if flag == 'message':
            jarvis_message = "Message sent successfully to " + name
           
        elif flag == 'voice call':
            message = ''
            jarvis_message = "Calling " + name
        else:
            message = ''
            jarvis_message = "Starting video call with " + name
           

        # Create WhatsApp URL and launch
        encoded_message = message.replace(' ', '%20')
        whatsapp_url = f"whatsapp://send?phone={mobile_no}&text={encoded_message}"
        full_command = f'start "" "{whatsapp_url}"'
        subprocess.run(full_command, shell=True)

        time.sleep(10)  # Wait for WhatsApp to open

        # Focus WhatsApp window
        if gw:
            try:
                for w in gw.getWindowsWithTitle('WhatsApp'):
                    w.activate()
                    time.sleep(1)
                    break
            except Exception as e:
                print("Window focus error:", e)

        # Perform action based on flag
        if flag == 'message':
            pyautogui.press('enter')
            rs=12.5
            msg="Successfully message sent " + name
            eel.receiverText(msg, rs)

        elif flag == 'voice call':
            print("Looking for voice_call.png on screen...")
            location = pyautogui.locateCenterOnScreen('voice_call.png', confidence=0.8)
            if location:
                pyautogui.moveTo(location)
                pyautogui.click()
                
            else:
                speak("Call icon not found.")

        elif flag == 'video':
            print("Looking for video_call.png on screen...")
            location = pyautogui.locateCenterOnScreen('video_call.png', confidence=0.8)
            if location:
                pyautogui.moveTo(location)
                pyautogui.click()
                rs=12.5
                msg="Successfully video called to "+ name
                eel.receiverText(msg, rs)
            else:
                speak("Video call icon not found.")

        speak(jarvis_message)

    except Exception as e:
        print("Error occurred:", e)
        speak("Something went wrong while using WhatsApp.")
        rs=0.1
        msg="Something went wrong while using WhatsApp."
        eel.receiverText(msg, rs)


    
def tell_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%I:%M %p")
    print(current_time)
    speak(f"The current time is {current_time}")
    eel.DisplayMessage(f"The current time is {current_time}")
    rs=3
    eel.receiverText(current_time, rs)

def tell_date():
    today = datetime.datetime.now()
    current_date = today.strftime("%A, %B %d, %Y")
    print(current_date)
    speak(f"Today's date is {current_date}")
    eel.DisplayMessage(f"Today's date is {current_date}")
    rs=3
    eel.receiverText(current_date, rs)


import requests
import eel
from backend.command import speak



def get_weather_report():
    speak("which city you want")
    city = takecommand()
    if not city:
        speak("Sorry, I couldn't detect your location.")
        eel.DisplayMessage("Location detection failed.")
        rs=0.6
        msg="Location detection failed."
        eel.receiverText(msg, rs)

        return

    api_key = "4f52320ee72838bb7cb8c7cbb701a3fe"
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if data["cod"] == 200:
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            report = f"Today’s weather in {city} is {temp}°C with {desc}."
            speak(report) 
            eel.DisplayMessage(report)
            rs=2
            eel.receiverText(report, rs)
        else:
            speak("Sorry, I couldn't fetch the weather.")
            eel.DisplayMessage("Weather information not available.")
            rs=1
            msg="Weather information not available."
            eel.receiverText(msg, rs)
    except Exception as e:
        print(f"Weather API error: {e}")
        speak("Weather service is not responding.")
        eel.DisplayMessage("Failed to connect to weather service.")
        rs=1
        msg="Failed to connect to weather service."
        eel.receiverText(msg, rs)
        
        

import webbrowser

def open_google_maps(query):
    trigger_phrases = ["show direction to", "navigate to", "go to", "direction to","take me to"]
    destination = None
    for phrase in trigger_phrases:
        if phrase in query.lower():
            destination = query.lower().split(phrase)[-1].strip()
            break

    if not destination:
        speak("Where do you want to go?")
        destination = takecommand()
        rs=1
        eel.receiverText(destination, rs)
        if not destination:
            speak("Sorry, I didn't catch the destination.")
            rs=0.1
            msg="Sorry, I didn't catch the destination."
            eel.receiverText(msg, rs)
            return

    speak("Which language do you prefer for navigation?")
    language = takecommand()
    rs=1
    eel.receiverText(language, rs)
    if not language:
        language = "english"  

    speak(f"Okay, using {language} for navigation preferences.")

    destination_url = destination.replace(" ", "+")
    url = f"https://www.google.com/maps/dir/?api=1&destination={destination_url}"

    webbrowser.open(url)
    speak(f"Showing directions to {destination}")
    rs=5
    msg=f"Showing directions to {destination}"
    eel.receiverText(msg, rs)
    


def open_calculator():
    os.system("start calc")
    rs=1.4
    msg="opened calculator"
    eel.receiverText(msg, rs)
    
    
def search_wikipedia(query):
    """Searches Wikipedia and returns a summary."""
    try:
        speak("Searching Wikipedia...")
        result = wikipedia.summary(query, sentences=2)
        speak(result)
        print(result)
    except wikipedia.exceptions.DisambiguationError:
        speak("Multiple results found. Please be more specific.")
        rs=1
        msg="Multiple results found. Please be more specific."
        eel.receiverText(msg, rs)
    except Exception:
        speak("I couldn't find anything on Wikipedia.")
        
        
        

genai.configure(api_key="AIzaSyD-KxurA5FWUpG5XaIcvSBtPgNbl2n13lE")


model = genai.GenerativeModel("gemini-1.5-flash")

@eel.expose
def handle_gemini_response(query: str):
    try:
        start_time = time.time()
        response = model.generate_content(query)
        end_time = time.time()
        elapsed = round(end_time - start_time, 2)
        final_response = response.text.strip()
        print(f"{final_response}\n\n{elapsed}s")
        speak(final_response)

        eel.receiverText(final_response, elapsed)

    except Exception as e:
        error_msg = f"Gemini Error: {str(e)}"
        print(error_msg)

        eel.receiverText(error_msg, 0.0)
        
def joke():
    
    joke=pyjokes.get_joke()
    print(f"{joke}")
    speak(joke)
    rs=5
    eel.receiverText(joke, rs)
    return joke

def screenshot() -> None:
    """Takes a screenshot and saves it."""
    img = pyautogui.screenshot()
    img_path = os.path.expanduser("C:\\Users\\91830\\OneDrive\\Desktop\\jarvisproject\\jarvis\\Pictures\\screenshot.png")
    img.save(img_path)
    # print(f"Screenshot saved as {img_path}.")
    speak(f"Screenshot saved as {img_path}.")
    
    
from threading import Thread
def set_reminder():
    speak("What time should I set the alarm for you?")

    command = takecommand().strip()
    print("Recognized command:", command)  

    # Normalize text: handle variations like p.m., P M, etc.
    command = command.upper()
    command = command.replace("A.M.", "AM").replace("P.M.", "PM")
    # Extract time using regex
    match = re.search(r'(\d{1,2}:\d{2})\s*(AM|PM)?', command)

    if match:
        time_part = match.group(1)
        meridiem = match.group(2)

        if not meridiem:
            speak("You didn't mention AM or PM. ")
            meridiem = takecommand()

        alarm_time = f"{time_part} {meridiem}"

        try:
            alarm_time_24 = datetime.strptime(alarm_time, "%I:%M %p").time()

            speak(f"Alarm is set for {alarm_time}")
            print(f"Alarm set for {alarm_time}")

            def alarm_checker():
                while True:
                    now = datetime.now().time().replace(second=0, microsecond=0)
                    if now == alarm_time_24:
                        try:
                            from backend.alarm import alarmpopup
                            alarmpopup(alarm_time)
                        except Exception as e:
                            print("Error:", e)
                            speak("Something went wrong triggering the alarm.")
                        break
                    time.sleep(30)

            Thread(target=alarm_checker, daemon=True).start()

        except ValueError:
            speak("Sorry, the time format is invalid. Please use the format like 10:00 AM or 9:30 PM.")
    else:
        speak("I couldn't understand the time. Please say something like 3:55 PM.")



import os
import pyautogui
import re
import datetime
import time

def get_hour_minute(query):
    # Normalize AM/PM (handles cases like "a.m", "p m", "P.M." etc.)
    query = query.upper()
    query = re.sub(r'\bA\.?M\.?\b', 'AM', query)
    query = re.sub(r'\bP\.?M\.?\b', 'PM', query)
    query = query.replace("A M", "AM").replace("P M", "PM")

    # Use regex to extract time and AM/PM
    match = re.search(r'(\d{1,2})(?::(\d{2}))?\s*(AM|PM)?', query)
    if not match:
        return None, None

    hour = int(match.group(1))
    minute = int(match.group(2)) if match.group(2) else 0
    ampm = match.group(3)

    if ampm:
        ampm = ampm.lower()
        if ampm == "pm" and hour != 12:
            hour += 12
        elif ampm == "am" and hour == 12:
            hour = 0

    return hour, minute

@eel.expose
def set_alarm_gui():
    speak("At what time should I set the alarm?")
    command = takecommand()
    # speak("AM or PM")
    # com = takecommand() 
    
    hour, minute = get_hour_minute(command)
    if hour is None:
        speak("I didn't understand the time. Please try again.")
        return

    # Step 1: Open Clock app (Windows)
    speak("Opening Clock app...")
    import os
    os.system("start ms-clock:")
    time.sleep(3)  # Wait for app to open

    # Step 2: GUI Automation using pyautogui
    speak(f"Setting alarm for {hour}:{minute:02d}...")
    
    pyautogui.click(90,26)
    time.sleep

    pyautogui.click(139,177)
    time.sleep(1)

    pyautogui.click(606,603)
    time.sleep(1)


    # Click on hour field
    pyautogui.click(229, 262)
    pyautogui.write(str(hour % 12 or 12), interval=0.1)  # Convert to 12-hour format

    # Click on minute field
    pyautogui.click(358, 264)
    pyautogui.write(f"{minute:02d}", interval=0.1)

    # Click AM/PM
    pyautogui.click(486, 259)
    time.sleep(0.5)
    # Step 2: Double click to cycle and force AM
    pyautogui.click(486, 259)
    time.sleep(0.5)
    

    # Step 3: If user wants PM, toggle once more
    if hour >= 12:
        pyautogui.click(486, 259)
        time.sleep(0.5)

    # Click Save (tick)
    pyautogui.click(296, 613)  # Adjust to your Save button position
    time.sleep(1)
    pyautogui.click(626, 22)
    msg="Alarm set successfully."
    print("Alarm set successfully.")
    rs=10
    eel.receiverText(msg, rs)
    
    
    

def jiosaavn():
    speak("which song you want to play")
    query = takecommand()
      # Converts "na gaju bomma" → "na+gaju+bomma"
    webbrowser.open(f'https://www.jiosaavn.com/')
    time.sleep(10)
    pyautogui.click(1029, 130)
    time.sleep(10)
    pyautogui.write(query,interval=0.1)
    time.sleep(2)
    pyautogui.click(242, 260)
    rs=5
    msg=f"This {query} song is played"
    eel.receiverText(msg, rs)





def ms_word():
    speak("What do you want me to write?")
    script = takecommand()

    speak("Opening Microsoft Word")
    os.startfile(r"C:\Program Files\Microsoft Office\root\Office16\WINWORD.EXE")

    # Wait for Word to launch
    time.sleep(5)

    # Try to bring Word window to front
    word_window = None
    for window in gw.getWindowsWithTitle('Word'):
        word_window = window
        if window.isMinimized:
            window.restore()
        window.activate()
        break

    if not word_window:
        speak("Couldn't bring Word to the front. Typing might not work.")
    else:
        time.sleep(5)  # let the window come to front
    # pyautogui.click(529,267)
    # time.sleep(3)
    pyautogui.click(650,389)
    time.sleep(3)
    # Type the script
    pyautogui.write(script, interval=0.1)

    # Simulate saving the file using keyboard (Ctrl+S)
    pyautogui.hotkey('ctrl', 's')
    time.sleep(2)

    # Type the filename
    filename = "newproject"
    pyautogui.write(filename, interval=0.1)
    time.sleep(2)

    # Press Enter to save
    pyautogui.press('enter')
    time.sleep(14)
    
    pyautogui.click(1708, 160)
    

    speak("File saved successfully.")
    rs=5
    msg="File saved successfully."
    eel.receiverText(msg, rs)
    
    
def wishme() -> None:
    """Greets the user based on the time of day."""
    speak("Welcome back !")
    print("Welcome back !")

    hour = datetime.datetime.now().hour
    if 4 <= hour < 12:
        speak("Good morning!")
        print("Good morning!")
    elif 12 <= hour < 16:
        speak("Good afternoon!")
        print("Good afternoon!")
    elif 16 <= hour < 24:
        speak("Good evening!")
        print("Good evening!")
    else:
        speak("Good night, see you tomorrow.")


