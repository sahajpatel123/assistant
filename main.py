import speech_recognition as sr
import time
import subprocess
import psutil
from actions import speak, make_call, open_news_globe
from display_manager import setup_workspace, go_dark

def get_system_pulse():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    return f"CPU is at {cpu} percent, Memory usage is {ram} percent, Sir."

def process_command(command_text):
    command = command_text.lower()
    print(f"Executing protocol: '{command}'")
    
    if "workspace" in command or "set up" in command:
        speak("Initializing the development arrays across both displays, Sir. Please stand by.")
        status = setup_workspace()
        speak(status)
        subprocess.run(["open", "http://127.0.0.1:5050/"])

    elif "go dark" in command or "lock" in command:
        speak("Executing security protocol. Going dark.")
        go_dark()

    elif "pulse" in command or "status" in command:
        pulse = get_system_pulse()
        speak(pulse)

    elif "news" in command:
        speak("Assembling the global intelligence report, Sir.")
        subprocess.run(["open", "http://127.0.0.1:5050/globe"])

    else:
        speak("I am monitoring, Sir, but that command is not in my current library.")

def listen_loop():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        print("CHRISTIN ONLINE. Waiting for wake word...")
        
    while True:
        try:
            with mic as source:
                audio = recognizer.listen(source, timeout=1, phrase_time_limit=3)
            text = recognizer.recognize_google(audio).lower()
            
            if "christin" in text:
                speak("I am here, Sir.")
                with mic as source:
                    command_audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    command_text = recognizer.recognize_google(command_audio)
                    process_command(command_text)
                    
        except Exception:
            pass

if __name__ == "__main__":
    # Start UI in background (User must run flask app separately or we can spawn it)
    # speak("System initialization complete. Good morning, Sir.")
    listen_loop()