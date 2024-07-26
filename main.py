import pyttsx3
import speech_recognition as sr
import keyboard
import os
import subprocess as sp
from datetime import datetime
from decouple import config
from random import choice
from conv import random_text
from online import find_my_ip, search_on_google, search_on_wikipedia, youtube, send_email, get_news, weather_forecast

engine = pyttsx3.init('sapi5')
engine.setProperty('volume', 1.5)
engine.setProperty('rate', 225)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

USER = config('USER')
HOSTNAME = config('BOT')


def speak(text):
    engine.say(text)
    engine.runAndWait()


def greet_me():
    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"Good Morning {USER}")
    elif (hour > +12) and (hour <= 16):
        speak(f"Good Afternoon {USER}")
    elif (hour >= 16) and (hour < 19):
        speak(f"Good Evening {USER}")
    speak(f"I am {HOSTNAME}. Hoy may i assist you? {USER}")


listening = False


def start_listening():
    global listening
    listening = True
    print(" started listening")


def pause_listining():
    global listening
    listening = False
    print(" stopped listening")


keyboard.add_hotkey('ctrl+alt+k', start_listening)
keyboard.add_hotkey('ctrl+alt+p', pause_listining)


def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        queri = r.recognize_google(audio, language='en-in')
        print(queri)
        if not 'stop' in queri or 'exit' in queri:
            speak(choice(random_text))
        else:
            hour = datetime.now().hour
            if hour >= 21 and hour < 6:
                speak("Good night sir,take care!")
            else:
                speak("Have a good day sir!")
            exit()

    except Exception:
        speak("Say that again please...")
        queri = 'None'
    return queri


if __name__ == '__main__':
    greet_me()
    while True:
        if listening:
            query = take_command().lower()
            if "how are you" in query:
                speak("I'm fine, what should I do?")
            elif "open command prompt" in query:
                speak("Opening command prompt")
                os.system('start cmd')
            elif "open camera" in query:
                speak("Opening camera")
                sp.run('start microsoft.windows.camera:', shell=True)

            elif "open notepad" in query:
                speak("Opening notepad")
                notepad_path = "C:\Windows"
                os.startfile(notepad_path)

            elif "open chrome" in query:
                speak("Opening chrome")
                chrome_path = "C:\Program Files\Google\Chrome\Application\chrome.exe"
                os.startfile(chrome_path)

            elif "ip address" in query:
                ip_address = find_my_ip()
                speak(
                    f"Your IP address is {ip_address}"
                )
                print(f"your Ip address is{ip_address}")

            elif "youtube" in query:
                speak("What do you want to play on you tube?")
                video = take_command().lower()
                youtube(video)

            elif "open google" in query:
                speak("What do you want to search on google {USER}")
                query = take_command().lower()
                search_on_google(query)

            elif "wikipedia" in query:
                speak("what do you want to search on wikipedia?")
                search = take_command().lower()
                results = search_on_wikipedia(search)
                speak(f"According to wikipedia,{results}")
                speak("I am printing in our terminal")
                print(results)


            elif "send an email" in query:
                speak("What do you want to send.Please enter in terminal")
                receiver_add = input("Email address:")
                speak("What should be the subject of the email")
                subject = take_command().capitalize()
                speak("What should be the body of the email")
                message = take_command().capitalize()
                if send_email(receiver_add, subject, message):
                    speak("I have sent the email")

                else:
                    speak("Something went wrong please try again")


            elif "give me news" in query:
                speak(f"I am reading out  the latest headline of today")
                speak(get_news())
                speak("I am printing it on screen")
                print(*get_news(), sep='\n')


            elif "weather" in query:
                ip_address = find_my_ip()
                speak("tell me the name of your city on screen")
                city = input("Enter name of your city :")
                speak(f"Getting weather report of your city {city}")
                weather, temp, feels_like = weather_forecast(city)
                speak(f"The current temprature is {temp}, but it feels like {feels_like}")
                speak(f"Also the weather report talks about {weather}")
                speak("I am printing weather information on screen")
                print(f"Description: {weather}\nTemprature: {temp}\nFeels like: {feels_like}")

            elif "calculate" in query:
                app_id = "Q5TEUK-R3VJ9XU38H"
                client = wolframalpha.Client(app_id)
                ind = query.lower().split().index("calculate")
                text = query.split()[ind+1:]
                result = client.query(" ".join(text))
                try:
                    ans = next(rsult.results).text
                    speak("The answer is "+ ans)
                    print("The answer is" + ans)
                except StopIteration:
                    speak("I couldn't understand your query. Please try again")

            elif "what is" in query or 'who is' in query or 'which is' in query:
                app_id = "Q5TEUK-R3VJ9XU38H"
                client = wolframalpha.Client(app_id)
                try:
                    ind = query.lower().index('what is') if 'what is' in query.lower() else \
                        query.lower().index('who is') if 'who is' in query.lower() else \
                            query.lower().index('which is') if 'which is' in query.lower() else None

                    if ind is not None:
                        text = query.split()[ind+2:]
                        res = client.query(" ".join(text))
                        ans = next(result.results).text
                        speak("The answer is "+ ans)
                        print("The answer is" + ans)
                    else:
                        speak("I coul not find that")

                except StopIteration:
                    speak("I couldn't understand your query. Please try again")
