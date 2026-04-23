import speech_recognition as sr
import time
import subprocess
import psutil
import os
import datetime
from actions import speak, make_call
from display_manager import setup_workspace, go_dark
from music_manager import control_apple_music, control_spotify, set_volume
from home_manager import trigger_home_scene
from vision_manager import verify_user, capture_and_analyze_screen
from intent_engine import get_intent
from briefing_manager import generate_morning_briefing
from memory_manager import memory
import automation_manager

# Configuration
REQUIRE_FACE = True # Set to True to enable facial recognition security
last_briefing_date = None

def get_system_pulse():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    return f"CPU is at {cpu} percent, Memory usage is {ram} percent, Sir."

def process_command(command_text):
    # Store user command in memory
    memory.add_interaction("user", command_text)
    
    intent_data = get_intent(command_text)
    intent = intent_data.get("intent")
    params = intent_data.get("params", {})
    
    response_text = ""
    print(f"Executing protocol: '{intent}' with params: {params}")
    
    if intent == "setup_workspace":
        speak("Initializing the development arrays across both displays, Sir. Please stand by.")
        status = setup_workspace()
        speak(status)
        subprocess.run(["open", "http://127.0.0.1:5050/"])
        response_text = status

    elif intent == "go_dark":
        speak("Executing security protocol. Going dark.")
        go_dark()
        response_text = "System locked."

    elif intent == "get_status":
        pulse = get_system_pulse()
        speak(pulse)
        response_text = pulse

    elif intent == "get_news":
        topic = params.get("topic", "")
        speak(f"Assembling the global intelligence report on {topic if topic else 'the latest events'}, Sir.")
        subprocess.run(["open", f"http://127.0.0.1:5050/globe?q={topic}"])
        response_text = "News interface displayed."

    elif intent == "play_music":
        player = params.get("player", "Music")
        action = params.get("action", "play")
        playlist = params.get("playlist")
        if player == "Spotify":
            status = control_spotify(action, playlist)
        else:
            status = control_apple_music(action, playlist)
        speak(status)
        response_text = status

    elif intent == "home_control":
        scene = params.get("scene")
        status = trigger_home_scene(scene)
        speak(status)
        response_text = status

    elif intent == "system_volume":
        level = params.get("level", 50)
        status = set_volume(level)
        speak(status)
        response_text = status

    elif intent == "analyze_screen":
        question = params.get("question", "What do you see on my screen?")
        speak("Processing visual feed, Sir.")
        response = capture_and_analyze_screen(question)
        speak(response)
        response_text = response

    elif intent == "ui_automation":
        action = params.get("action")
        target = params.get("target")
        coords = params.get("coordinates", [])
        
        if action == "type":
            status = automation_manager.type_text(target)
        elif action == "click":
            if coords:
                status = automation_manager.click_at(coords[0], coords[1])
            else:
                status = "Sir, I require coordinates to perform a manual click."
        elif action == "press":
            status = automation_manager.press_key(target)
        else:
            status = "Automation protocol not recognized, Sir."
        
        speak(status)
        response_text = status

    elif intent == "general_query":
        speak(f"I am processing your request regarding '{command_text}', Sir.")
        from intent_engine import model
        if model:
            try:
                response = model.generate_content(command_text)
                speak(response.text)
                response_text = response.text
            except:
                speak("I encountered an error while processing your inquiry, Sir.")
                response_text = "Error in general query."
        else:
            speak("I am monitoring, Sir, but that command is not in my current library.")
            response_text = "Command not in library."

    else:
        speak("I am monitoring, Sir, but that command is not in my current library.")
        response_text = "Unknown intent."

    # Store assistant response in memory
    memory.add_interaction("assistant", response_text)

def listen_loop():
    global last_briefing_date
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
                # Security Check
                if REQUIRE_FACE:
                    faces_dir = "faces"
                    has_faces = os.path.exists(faces_dir) and any(f.endswith((".jpg", ".png")) for f in os.listdir(faces_dir))
                    
                    if has_faces:
                        speak("Verifying identity, Sir.")
                        if not verify_user():
                            speak("Unauthorized access detected. Saving intruder image and locking system.")
                            go_dark()
                            continue
                    else:
                        print("Facial recognition enabled but no known faces found in 'faces/' directory. Skipping verification.")

                # Morning Briefing Logic
                today = datetime.date.today()
                if last_briefing_date != today:
                    briefing = generate_morning_briefing()
                    speak(briefing)
                    last_briefing_date = today
                else:
                    speak("I am here, Sir.")
                    
                with mic as source:
                    command_audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                    command_text = recognizer.recognize_google(command_audio)
                    process_command(command_text)

        except Exception:
            pass

if __name__ == "__main__":
    listen_loop()
