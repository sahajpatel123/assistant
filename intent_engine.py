import os
import re
import json
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini if API key is present
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
else:
    model = None

from memory_manager import memory

def extract_intent_llm(text):
    """
    Uses Gemini to extract intent and parameters from natural language.
    """
    if not model:
        return None

    context = memory.get_recent_context(limit=5)

    prompt = f"""
    Analyze the following user command for a virtual assistant and return a JSON object with 'intent' and 'params'.
    
    RECENT CONTEXT:
    {context}

    Possible intents: 
    - setup_workspace (params: none)
    - go_dark (params: none)
    - get_status (params: none)
    - get_news (params: topic)
    - play_music (params: player['Music', 'Spotify'], action['play', 'pause', 'next', 'previous'], playlist)
    - home_control (params: scene, device, state)
    - system_volume (params: level[0-100])
    - analyze_screen (params: question)
    - ui_automation (params: action['type', 'click', 'press', 'find'], target, coordinates[x, y])
    - general_query (params: question)

    User command: "{text}"

    Return ONLY JSON.
    """
    
    try:
        response = model.generate_content(prompt)
        # Extract JSON from response text
        match = re.search(r'\{.*\}', response.text, re.DOTALL)
        if match:
            return json.loads(match.group())
    except Exception as e:
        print(f"LLM Error: {e}")
    return None

def extract_intent_local(text):
    """
    Fallback local intent extraction using regex/keywords.
    """
    text = text.lower()
    
    if any(k in text for k in ["workspace", "set up"]):
        return {"intent": "setup_workspace", "params": {}}
    
    if any(k in text for k in ["go dark", "lock", "sleep"]):
        return {"intent": "go_dark", "params": {}}
    
    if any(k in text for k in ["status", "pulse", "system"]):
        return {"intent": "get_status", "params": {}}
    
    if "news" in text:
        topic = text.replace("news", "").strip()
        return {"intent": "get_news", "params": {"topic": topic}}
    
    if any(k in text for k in ["music", "play", "spotify", "apple music"]):
        player = "Spotify" if "spotify" in text else "Music"
        action = "play"
        if "pause" in text or "stop" in text: action = "pause"
        if "next" in text: action = "next"
        if "previous" in text: action = "previous"
        return {"intent": "play_music", "params": {"player": player, "action": action}}
    
    if any(k in text for k in ["light", "home", "scene"]):
        return {"intent": "home_control", "params": {"scene": text}}

    if "volume" in text:
        match = re.search(r'(\d+)', text)
        level = int(match.group(1)) if match else 50
        return {"intent": "system_volume", "params": {"level": level}}

    if any(k in text for k in ["screen", "see", "what is on my screen", "look at"]):
        return {"intent": "analyze_screen", "params": {"question": text}}

    return {"intent": "general_query", "params": {"question": text}}

def get_intent(text):
    """
    Main entry point for intent extraction.
    """
    intent = extract_intent_llm(text)
    if not intent:
        intent = extract_intent_local(text)
    return intent
