import datetime
import os
import warnings
from dotenv import load_dotenv
from intel_manager import get_weather, get_calendar_events

# Suppress FutureWarnings globally
warnings.filterwarnings("ignore", category=FutureWarning)

load_dotenv()

# Use Grok for synthesis if available
from intent_engine import grok_client

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

    system_prompt = "You are Christin, a highly advanced, Jarvis-like AI assistant addressing your owner 'Sir'."
    user_prompt = f"""
    Current Time: {time_str}
    Date: {date_str}
    Environmental Data: {weather_info}
    Tactical Schedule: {calendar_info}
    
    Give a very brief, concise, and cool morning briefing. Keep it under 3 sentences. No markdown formatting, just plain text suitable for text-to-speech.
    """

    if not grok_client:
        return f"Good morning, Sir. It is {time_str} on {date_str}. {weather_info} Calendar status: {calendar_info}"

    try:
        completion = grok_client.chat.completions.create(
            model="grok-3",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
        )
        return completion.choices[0].message.content.replace("*", "")
    except Exception as e:
        print(f"Grok Briefing Error: {e}")
        return f"Good morning, Sir. It is {time_str}. All systems online."
