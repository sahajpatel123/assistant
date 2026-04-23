from intel_manager import get_weather, get_calendar_events
import datetime
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None


def generate_morning_briefing():
    """
    Generates a brief tactical morning update using an LLM.
    Includes real weather and calendar if keys are present.
    """
    now = datetime.datetime.now()
    time_str = now.strftime("%I:%M %p")
    date_str = now.strftime("%A, %B %d")

    weather_info = get_weather()
    calendar_info = get_calendar_events()

    if not model:
        return f"Good morning, Sir. It is {time_str} on {date_str}. {weather_info} Calendar status: {calendar_info}"

    prompt = f"""
    You are Christin, a highly advanced, Jarvis-like AI assistant addressing your owner "Sir".
    It is {time_str} on {date_str}.
    Environmental Data: {weather_info}.
    Tactical Schedule: {calendar_info}.

    Give a very brief, concise, and cool morning briefing. Keep it under 3 sentences. No markdown formatting, just plain text suitable for text-to-speech.
    """

    try:
        response = model.generate_content(prompt)
        return response.text.replace("*", "")
    except Exception as e:
        print(f"Briefing error: {e}")
        return f"Good morning, Sir. It is {time_str}. All systems online."
