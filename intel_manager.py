import requests
import os
import geocoder
from dotenv import load_dotenv

load_dotenv()

NEWS_API_KEY = os.getenv("NEWS_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

def get_real_news(topic=None):
    """
    Fetches real-time news from NewsAPI.
    """
    if not NEWS_API_KEY:
        return [{"headline": "News API Key missing in .env", "lat": 0, "lng": 0}]
    
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "apiKey": NEWS_API_KEY,
        "language": "en",
        "pageSize": 10
    }
    if topic:
        url = "https://newsapi.org/v2/everything"
        params["q"] = topic

    try:
        response = requests.get(url, params=params)
        data = response.json()
        articles = data.get("articles", [])
        
        news_items = []
        for art in articles:
            # NewsAPI doesn't provide lat/lng, so we'll randomize coordinates 
            # for the globe visualization while using real headlines
            news_items.append({
                "headline": art.get("title"),
                "lat": (os.urandom(1)[0] / 255 * 140) - 70,
                "lng": (os.urandom(1)[0] / 255 * 360) - 180,
                "source": art.get("source", {}).get("name")
            })
        return news_items if news_items else [{"headline": "No recent intel found, Sir.", "lat": 0, "lng": 0}]
    except Exception as e:
        print(f"News Fetch Error: {e}")
        return [{"headline": "Global news grid is offline, Sir.", "lat": 0, "lng": 0}]

def get_weather():
    """
    Fetches real-time weather based on IP location.
    """
    if not WEATHER_API_KEY:
        return "Weather API Key missing."

    try:
        g = geocoder.ip('me')
        city = g.city or "New York"
        
        url = f"http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": WEATHER_API_KEY,
            "units": "metric"
        }
        response = requests.get(url, params=params)
        data = response.json()
        
        temp = data["main"]["temp"]
        desc = data["weather"][0]["description"]
        return f"{temp} degrees with {desc} in {city}."
    except Exception as e:
        print(f"Weather Error: {e}")
        return "Unable to retrieve atmospheric data, Sir."

def get_calendar_events():
    """
    Placeholder for Google Calendar integration.
    Requires credentials.json and token.json.
    """
    # This is a complex setup, so we provide the logic but fall back gracefully
    if not os.path.exists("token.json"):
        return "Calendar sync requires authentication, Sir."
    
    # Logic for google-api-python-client would go here
    return "Your schedule is being synchronized, Sir."
