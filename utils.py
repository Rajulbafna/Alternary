import os
import requests
import folium
from streamlit_folium import folium_static
from dotenv import load_dotenv

load_dotenv()

LOCATIONIQ_API_KEY = os.getenv("LOCATIONIQ_API_KEY")

# ===== Weather Helper =====
def get_weather_forecast(lat, lon):
    """
    Get 7-day weather forecast using Open-Meteo (free, no API key required).
    """
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "forecast_days": 7,
        "timezone": "auto"
    }
    try:
        r = requests.get(url, params=params)
        data = r.json()
        forecast = []
        for i in range(len(data["daily"]["time"])):
            forecast.append({
                "date": data["daily"]["time"][i],
                "temp_max": data["daily"]["temperature_2m_max"][i],
                "temp_min": data["daily"]["temperature_2m_min"][i],
                "precipitation": data["daily"]["precipitation_sum"][i]
            })
        return forecast
    except Exception as e:
        return [{"error": str(e)}]

# ===== Map Helper =====
def show_city_map(lat, lon, city_name):
    """
    Show an interactive map with Folium centered on the city.
    """
    try:
        m = folium.Map(location=[lat, lon], zoom_start=12)
        folium.Marker([lat, lon], popup=city_name).add_to(m)
        folium_static(m)
    except Exception as e:
        return f"Map error: {str(e)}"

# ===== Hotel Recommender (Mock) =====
def get_hotels(city):
    """
    For now, return a mock hotel list.
    """
    hotels = [
        {"name": f"{city} Grand Hotel", "price_inr": 5000, "rating": 4.5},
        {"name": f"{city} Budget Stay", "price_inr": 2500, "rating": 4.0},
        {"name": f"{city} Luxury Suites", "price_inr": 12000, "rating": 5.0}
    ]
    return hotels
