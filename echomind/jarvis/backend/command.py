import os
import pyttsx3
import time
import speech_recognition as sr 
import eel

def speak(text):
   text = str(text)
   engine = pyttsx3.init('sapi5')
   voices = engine.getProperty('voices')
   engine.setProperty('voice',voices[1].id)
   engine.setProperty('rate',174)
   eel.DisplayMessage(text)
   engine.say(text)
   eel.receiverText(text)
   engine.runAndWait()
   
@eel.expose  
def takecommand():
    
    r = sr.Recognizer()
    
    with sr.Microphone() as source:
        print('Listening.....')
        eel.DisplayMessage('Listening.....')
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source, 10 , 3 )
        
    try:
        print('Recognizing...')
        eel.DisplayMessage("recognizing.....")
        query = r.recognize_google(audio,language='en-in')
        print(f"user said:{query}")
        eel.DisplayMessage(query)
        time.sleep(2)
        
    except Exception as e:
        speak("Sorry, I did not catch that.")
        eel.DisplayMessage("Sorry, I did not catch that.")
        return ""
    return query.lower()

@eel.expose
def allCommands(message=1):
    
    if message ==1:
        
        query = takecommand()
        print(query)
        eel.senderText(query)
    else:
        query = message
        eel.senderText(query)
      
    
    try:
        
        if "open" in query or "search" in query:
            from backend.features import openCommand
            openCommand(query)
        elif "notepad" in query:
            os.system("start notepad")

        elif "on youtube" in query:
            from backend.features import PlayYoutube
            PlayYoutube(query)
            
        elif "time" in query:
            from backend.features import tell_time
            tell_time()

        elif "date" in query:
            from backend.features import tell_date
            tell_date()

        elif "weather" in query:
            from backend.features import get_weather_report
            get_weather_report()

        elif "Take me to" in query or "direction" in query or "maps" in query:
            from backend.features import open_google_maps
            open_google_maps(query)
            
        elif "shutdown" in query:
            speak("Shutting down the system, goodbye!")
            os.system("shutdown /s /f /t 1")
            
            
        elif "restart" in query:
            speak("Restarting the system, please wait!")
            os.system("shutdown /r /f /t 1")
            
        elif "calculator" in query:
            from backend.features import open_calculator
            speak("Opening calculator")
            open_calculator()
            os.system("start calc")
            return
        
        elif "tell me a joke" in query:
            from backend.features import joke
            joke()
            
        elif "wikipedia" in query:
            from backend.features import search_wikipedia
            query = query.replace("wikipedia", "").strip()
            search_wikipedia(query)    
        
        elif "offline" in query or "exit" in query:
            speak("Going offline. Have a good day!")
            
        elif "microsoft word" in query :
            from backend.features import ms_word
            ms_word()
            
        # elif "screenshot" or "take screenshot" in query:
        #     from backend.features import screenshot
        #     screenshot()
        
        elif "set reminder" in query:
            from backend.features import set_reminder
            set_reminder()
        elif "set alarm" in query:
            from backend.features import set_alarm_gui
            set_alarm_gui()
        elif "play song" in query:
            from backend.features import jiosaavn
            jiosaavn()  


        elif "powerpoint" in query or "open powerpoint" in query:
            from backend.features import open_powerpoint
            open_powerpoint()
     
        elif "send message" in query or "phone call" in query or "video call" in query:
            from backend.features import findContact, whatsApp
            contact_no, name = findContact(query)

            if contact_no != 0:
                flag = ''
                message = ''

                if "send message" in query:
                    flag = 'message'
                    speak("What message should I send?")
                    message = takecommand()

                elif "voice call" in query:
                    flag = 'call'

                elif "video call" in query:
                    flag = 'video'

                whatsApp(contact_no, message, flag, name)
            else:
                speak("Sorry, I couldn't find that contact.")

        else:
            
            from backend.features import handle_gemini_response
            handle_gemini_response(query)
            
            
    except Exception as e:
        print(f"Error occurred: {e}")

    eel.showHood()













