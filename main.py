import warnings
import os
import sys

# Critical: Silence AI SDK warnings and kill GRPC flooding
warnings.filterwarnings("ignore", category=FutureWarning)
os.environ["GRPC_ENABLE_FORK_SUPPORT"] = "0"

import speech_recognition as sr
import time
import subprocess
import psutil
import datetime
import requests
from contextlib import contextmanager

# Professional Hardware Suppression: Silences AUHAL/PortAudio noise in terminal
@contextmanager
def ignore_stderr():
    """Redirects stderr to devnull to prevent terminal flooding from hardware warnings."""
    devnull = os.open(os.devnull, os.O_WRONLY)
    old_stderr = os.dup(sys.stderr.fileno())
    try:
        os.dup2(devnull, sys.stderr.fileno())
        yield
    finally:
        os.dup2(old_stderr, sys.stderr.fileno())
        os.close(devnull)
        os.close(old_stderr)

from actions import speak, make_call
from display_manager import setup_workspace, go_dark
from music_manager import control_apple_music, control_spotify, set_volume
from home_manager import trigger_home_scene
from vision_manager import verify_user, capture_and_analyze_screen
from intent_engine import get_intent
from briefing_manager import generate_morning_briefing
from memory_manager import memory
from knowledge_manager import knowledge
import automation_manager

# Configuration
REQUIRE_FACE = True # Set to True to enable facial recognition security
last_briefing_date = None

def get_system_pulse():
    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent
    return f"CPU is at {cpu} percent, Memory usage is {ram} percent, Sir."

def push_ui_update(command, response):
    """Sends the command and response to the Flask HUD for display."""
    try:
        requests.post("http://127.0.0.1:5050/api/update_status", 
                      json={"command": command, "response": response},
                      timeout=1)
    except:
        pass

def process_command(command_text):
    # Store user command in memory
    memory.add_interaction("user", command_text)
    
    intent_data = get_intent(command_text)
    intent = intent_data.get("intent")
    params = intent_data.get("params", {})
    
    response_text = ""
    print(f"Executing protocol: '{intent}' with params: {params}")
    
    if intent == "setup_workspace":
        status = setup_workspace()
        response_text = status
        push_ui_update(command_text, response_text)
        speak(status)
        subprocess.run(["open", "http://127.0.0.1:5050/"])

    elif intent == "go_dark":
        response_text = "System locked."
        push_ui_update(command_text, response_text)
        speak("Executing security protocol. Going dark.")
        go_dark()

    elif intent == "get_status":
        pulse = get_system_pulse()
        response_text = pulse
        push_ui_update(command_text, response_text)
        speak(pulse)

    elif intent == "get_news":
        topic = params.get("topic", "")
        response_text = f"News grid active for {topic if topic else 'Global Headlines'}."
        push_ui_update(command_text, response_text)
        speak(f"Assembling the global intelligence report on {topic if topic else 'the latest events'}, Sir.")
        
        try:
            from display_manager import move_window
            subprocess.run(["open", "-a", "Google Chrome", f"http://127.0.0.1:5050/globe?q={topic}"], check=True)
            time.sleep(1)
            move_window("Google Chrome", 0, 0, 1400, 900)
            
            subprocess.run(["open", "-n", "-a", "Google Chrome", "--args", "--new-window", f"http://127.0.0.1:5050/news_dashboard?q={topic}"])
            time.sleep(1)
            move_window("Google Chrome", 1800, 0, 1920, 1080)
        except:
            subprocess.run(["open", f"http://127.0.0.1:5050/globe?q={topic}"])
            subprocess.run(["open", f"http://127.0.0.1:5050/news_dashboard?q={topic}"])

    elif intent == "play_music":
        player = params.get("player", "Music")
        action = params.get("action", "play")
        playlist = params.get("playlist")
        if player == "Spotify":
            status = control_spotify(action, playlist)
        else:
            status = control_apple_music(action, playlist)
        response_text = status
        push_ui_update(command_text, response_text)
        speak(status)

    elif intent == "home_control":
        scene = params.get("scene")
        status = trigger_home_scene(scene)
        response_text = status
        push_ui_update(command_text, response_text)
        speak(status)

    elif intent == "system_volume":
        level = params.get("level", 50)
        status = set_volume(level)
        response_text = status
        push_ui_update(command_text, response_text)
        speak(status)

    elif intent == "analyze_screen":
        speak("Processing visual feed, Sir.")
        response = capture_and_analyze_screen(params.get("question", "What is on my screen?"))
        response_text = response
        push_ui_update(command_text, response_text)
        speak(response)

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
        
        response_text = status
        push_ui_update(command_text, response_text)
        speak(status)

    elif intent == "knowledge_query":
        question = params.get("question", command_text)
        speak("Searching my neural knowledge base, Sir.")
        context = knowledge.query_knowledge(question)
        if context:
            from intent_engine import grok_client
            prompt = f"Using the following context, answer the user's question: {question}\n\nCONTEXT:\n{context}"
            try:
                completion = grok_client.chat.completions.create(
                    model="grok-3",
                    messages=[
                        {"role": "system", "content": "You are Christin, a highly advanced AI assistant. Answer using the provided context."},
                        {"role": "user", "content": prompt},
                    ],
                )
                response_text = completion.choices[0].message.content
                push_ui_update(command_text, response_text)
                speak(response_text)
            except Exception as e:
                print(f"Grok Knowledge Error: {e}")
                response_text = "Analysis synthesis failed."
                push_ui_update(command_text, response_text)
                speak("I found relevant data but failed to synthesize an answer, Sir.")
        else:
            response_text = "No relevant memory found."
            push_ui_update(command_text, response_text)
            speak(
                "I could not find any relevant information in my long-term memory, Sir.")

    elif intent == "knowledge_ingest":
        path = params.get("file_path")
        if not path:
            status = "Sir, I require a file path to begin the indexing protocol."
        else:
            status = knowledge.ingest_file(path)
        
        response_text = status
        push_ui_update(command_text, response_text)
        speak(status)

    elif intent == "general_query":
        speak(f"Processing, Sir.")
        # Check knowledge base first (RAG)
        context = knowledge.query_knowledge(command_text)
        from intent_engine import grok_client
        if grok_client:
            prompt = command_text
            if context:
                prompt = f"Using the following context if relevant, answer the question: {command_text}\n\nCONTEXT:\n{context}"
            try:
                completion = grok_client.chat.completions.create(
                    model="grok-3",
                    messages=[
                        {"role": "system", "content": "You are Christin, a highly advanced AI assistant built for Sir."},
                        {"role": "user", "content": prompt},
                    ],
                )
                response_text = completion.choices[0].message.content
                push_ui_update(command_text, response_text)
                speak(response_text)
            except Exception as e:
                print(f"Grok General Query Error: {e}")
                response_text = "Brain error."
                push_ui_update(command_text, response_text)
                speak("I encountered an error while processing your inquiry, Sir.")
        else:
            response_text = "Cognitive engine offline."
            push_ui_update(command_text, response_text)
            speak("I am monitoring, Sir, but that command is not in my current library.")

    else:
        response_text = "Intent not recognized."
        push_ui_update(command_text, response_text)
        speak("I am monitoring, Sir, but that command is not in my current library.")

    # Store assistant response in memory
    memory.add_interaction("assistant", response_text)

def listen_loop():
    global last_briefing_date
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = True
    recognizer.energy_threshold = 300 # Baseline sensitivity
    
    # Calibration with suppression
    with ignore_stderr():
        mic = sr.Microphone()
        with mic as source:
            recognizer.adjust_for_ambient_noise(source, duration=2)
            print("CHRISTIN ONLINE. Monitoring frequencies...")

    while True:
        try:
            with ignore_stderr():
                with mic as source:
                    # Optimized listen for MacOS hardware
                    audio = recognizer.listen(source, timeout=1, phrase_time_limit=4)
            
            # Use en-US for maximum wake-word accuracy
            text = recognizer.recognize_google(audio, language="en-US").lower()
            print(f"Captured: '{text}'") # Debug line for Sir
            command_text = text.strip()

            if command_text:
                if REQUIRE_FACE:
                    faces_dir = "faces"
                    has_faces = os.path.exists(faces_dir) and any(
                        f.endswith((".jpg", ".png")) for f in os.listdir(faces_dir))

                    if has_faces:
                        if not verify_user():
                            speak(
                                "Unauthorized access detected. Saving intruder image and locking system.")
                            go_dark()
                            continue
                    else:
                        print("Facial recognition enabled but no known faces found in 'faces/' directory. Skipping verification.")

                # Morning Briefing Logic
                today = datetime.date.today()
                if last_briefing_date != today:
                    briefing = generate_morning_briefing()
                    # Push morning briefing to UI
                    push_ui_update("System Wake", briefing)
                    speak(briefing)
                    last_briefing_date = today

                process_command(command_text)

        except Exception:
            pass

if __name__ == "__main__":
    listen_loop()
