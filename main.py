import speech_recognition as sr
import pyttsx3
import os
import google.generativeai as genai
import webbrowser
import datetime
import sys

try:
    genai.configure(api_key = os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("models/gemini-2.5-pro")
except Exception as e:
    print(f"Error initializing Gemini client. Details: {e}")
    sys.exit()

r = sr.Recognizer()

def speak(audio):
    print(f"XADEN:{audio}")
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.setProperty('rate', 175)
    engine.say(audio)
    engine.runAndWait()

def take_command():

    with sr.Microphone() as source:
        print("\nListening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source,duration=0.5)
        try:
            audio = r.listen(source)
            print("Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            print(f"Admin: {query}\n")
            return query.lower()
        except sr.UnknownValueError:
            print("Sorry could not hear that")
            return "none"
        except sr.RequestError:
            print("Could not request results")
            return "none"
        except Exception as e:
            print(f"An error occurred: {e}")
            return "None"

def handle_query(query):
    if "open google chrome" in query:
        os.startfile("C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe")
        speak("Opening Google Chrome.")

    elif "open spotify" in query:
        os.system("Spotify")
        speak("Opening Spotify")

    elif "open youtube" in query:
        webbrowser.open("https://www.youtube.com")
        speak("Opening YouTube.")

    elif "open instagram" in query:
        webbrowser.open("https://www.instagram.com")
        speak("Opening Instagram.")

    elif "time" in query:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {current_time}")

    elif "date" in query:
        today = datetime.datetime.now().strftime("%A, %d %B %Y")
        speak(f"Today is {today}")

    elif "log out" in query or "sign out" in query:
        speak("Logging out...")
        sys.exit()

    else:
        try:
            
            response_stream = model.generate_content(query, stream=True)
            
            full_response = ""
            sentence_buffer = ""
            
            for chunk in response_stream:
                full_response += chunk.text
                sentence_buffer += chunk.text

                if any(p in sentence_buffer for p in ".!?"):
                    speak(sentence_buffer.strip())
                    sentence_buffer = "" 
            
            if sentence_buffer.strip():
                speak(sentence_buffer.strip())

        except Exception as e:
            speak("Sorry, I couldn't get a response")
            print(f"Error: {e}")

if __name__ == "__main__":
    speak("Initializing XADEN...")
    speak("Hello. How can I help you today?")
    
    while True:
        query = take_command()

        if not query or query == "none":
            continue  
        
        try:
            handle_query(query)
        except Exception as e:
            print(f"Error while handling query: {e}")
            speak("Sorry, an error occurred while processing that.")
