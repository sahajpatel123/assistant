import datetime
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
    Includes mock weather and current time.
    """
    now = datetime.datetime.now()
    time_str = now.strftime("%I:%M %p")
    date_str = now.strftime("%A, %B %d")

    # In a real app, you'd pull weather and calendar from APIs
    mock_weather = "Clear skies, 22 degrees Celsius."
    mock_calendar = "One meeting at 10 AM."

    if not model:
        return f"Good morning, Sir. It is {time_str} on {date_str}. {mock_weather} You have {mock_calendar} Have a productive day."

    prompt = f"""
    You are Christin, a highly advanced, Jarvis-like AI assistant addressing your owner "Sir".
    It is {time_str} on {date_str}.
    The weather is: {mock_weather}.
    Calendar: {mock_calendar}.
    
    Give a very brief, concise, and cool morning briefing. Keep it under 3 sentences. No markdown formatting, just plain text suitable for text-to-speech.
    """

    try:
        response = model.generate_content(prompt)
        return response.text.replace("*", "")
    except Exception as e:
        print(f"Briefing error: {e}")
        return f"Good morning, Sir. It is {time_str}. All systems online."
