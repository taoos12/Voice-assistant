import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import time
import subprocess
from ecapture import ecapture as ec
import wolframalpha
import requests

# Initialize the speech engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0] .id)  # 0 for male and 1 for female

def speak(text):
    engine.say(text)
    engine.runAndWait()

def wishMe():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Hello, Good Morning")
        print("Hello, Good Morning")
    elif 12 <= hour < 18:
        speak("Hello, Good Afternoon")
        print("Hello, Good Afternoon")
    else:
        speak("Hello, Good Evening")
        print("Hello, Good Evening")

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

        try:
            statement = r.recognize_google(audio, language='en-in')
            print(f"user said: {statement}\n")
        except Exception as e:
            speak("Pardon me, please say that again")
            return "None"
        return statement.lower()

def download_file(url, local_filename):
    # Send a HTTP request to the URL
    with requests.get(url, stream=True) as response:
        # Raise an exception if the request returned an unsuccessful status code
        response.raise_for_status()
        # Open the local file in binary write mode
        with open(local_filename, 'wb') as file:
            # Write the response content to the file in chunks
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
    return local_filename

print("Loading your personal AI assistant ")
speak("Loading your personal AI assistant ")
wishMe()

if __name__ == '__main__':
    while True:
        speak("Tell me how can I help you now?")
        statement = takeCommand()
        if statement == 0:
            continue

        if "good bye" in statement or "ok bye" in statement or "stop" in statement or "Get lost" in statement or "Bye" in statement or "Tata" in statement:
            speak('your personal assistant is shutting down, Good bye')
            print('your personal assistant is shutting down, Good bye')
            break

        elif 'wikipedia' in statement:
            speak('Searching Wikipedia...')
            statement = statement.replace("wikipedia", "")
            results = wikipedia.summary(statement, sentences=3)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in statement:
            webbrowser.open("https://www.youtube.com")
            speak("YouTube is open now")
            time.sleep(3)

        elif 'open google' in statement:
            webbrowser.open("https://www.google.com")
            speak("Google Chrome is open now")
            time.sleep(3)

        elif 'open gmail' in statement:
            webbrowser.open("https://mail.google.com")
            speak("Google Mail is open now")
            time.sleep(3)

        elif 'time' in statement:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"The time is {strTime}")

        elif 'news' in statement:
            webbrowser.open("https://timesofindia.indiatimes.com/home/headlines")
            speak('Here are some headlines from the Times of India, Happy reading')
            time.sleep(3)

        elif "camera" in statement or "take a photo" in statement:
            ec.capture(0, "robo camera", "img.jpg")

        elif 'search' in statement:
            statement = statement.replace("search", "")
            webbrowser.open(statement)
            time.sleep(3)

        elif 'ask' in statement:
            speak('I can answer computational and geographical questions. What question do you want to ask now?')
            question = takeCommand()
            app_id = "YOUR_WOLFRAMALPHA_APP_ID"
            client = wolframalpha.Client(app_id)
            try:
                res = client.query(question)
                answer = next(res.results).text
                speak(answer)
                print(answer)
            except Exception as e:
                speak("Sorry, I couldn't find an answer for that question.")
                print("Error:", e)

        elif 'who are you' in statement or 'hu r u' in statement or 'what can you do' in statement or 'are you' in statement:
            speak('I am a personal assistants, I am designed to help the users with a wide range of tasks. Here are some things I can do: Answer Questions, Help with Writing and Editing, Provide Summaries, Translate Text,Tutoring and Homework Help, Generate Creative Content, Assist with Coding and Debugging, Organize Tasks and Reminders, Conduct Research, Give Recommendations, Engage in Conversations , Offer General Wellness Tips and many more')

        elif "made you" in statement or "created you" in statement or "discovered you" in statement:
            speak("I was built by Taoos ")
            print("I was built by Taoos")
            time.sleep(3)

        elif "weather" in statement:
            api_key = "42c15f5a163b4407874114236240308"
            base_url = "http://api.weatherapi.com/v1/current.json"
            speak("What is the city name?")
            city_name = takeCommand()
            complete_url = f"{base_url}?key={api_key}&q={city_name}"
            response = requests.get(complete_url)
            x = response.json()
            if "error" not in x:
                current_temperature = x["current"]["temp_c"]
                current_humidity = x["current"]["humidity"]
                weather_description = x["current"]["condition"]["text"]
                speak(f"Temperature in Celsius is {current_temperature}, "
                      f"humidity in percentage is {current_humidity}, "
                      f"description: {weather_description}")
                print(f"Temperature in Celsius = {current_temperature}\n"
                      f"Humidity (in percentage) = {current_humidity}\n"
                      f"Description = {weather_description}")
            else:
                speak("City not found. Please try again.")
                print("City not found")

        elif 'download' in statement:
            speak('Please provide the URL of the file you want to download.')
            file_url = takeCommand()
            speak('Please provide the name to save the file as.')
            file_name = takeCommand()
            try:
                speak(f"Downloading file from {file_url}...")
                download_file(file_url, file_name)
                speak(f"File downloaded successfully as {file_name}")
                print(f"File downloaded successfully as {file_name}")
            except Exception as e:
                speak("Sorry, there was an error downloading the file.")
                print("Error:", e)

        elif "log off" in statement or "sign out" in statement:
            speak("Ok, your PC will log off in 10 seconds. Make sure you exit from all applications.")
            subprocess.call(["shutdown", "/l"])

        time.sleep(3)
