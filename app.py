import streamlit as st
from agents import (
    city_selector_agent,
    local_expert_agent,
    trip_planner_agent,
    budget_manager_agent,
    flight_price_agent,
    chatbot_agent,
    geocode_city
)
from utils import get_weather_forecast, show_city_map, get_hotels

# ===== App Title =====
st.set_page_config(page_title="NavMind - AI Travel Planner", layout="wide")
st.title("🌍 NavMind: AI-Powered Travel Planner")

# ===== User Input =====
st.sidebar.header("Your Travel Preferences")
travel_type = st.sidebar.selectbox("Travel Type", ["Leisure", "Business"])
interests = st.sidebar.selectbox("Interests", ["Beach", "History", "Food"])
season = st.sidebar.selectbox("Preferred Season", ["Summer", "Winter", "Monsoon"])
budget_inr = st.sidebar.number_input("Total Budget (INR)", min_value=5000, step=1000)
days = st.sidebar.slider("Number of Days", min_value=2, max_value=14, value=5)
departure_city_code = st.sidebar.text_input("Departure Airport Code (IATA)", value="DEL")

if st.sidebar.button("Plan My Trip"):
    # ===== Select Cities =====
    st.subheader("🏙 Recommended Cities")
    suggested_cities = city_selector_agent(interests, season)
    st.write(suggested_cities)
    
    chosen_city = st.selectbox("Choose Your City", suggested_cities)
    
    # ===== Local Info =====
    st.subheader(f"📖 About {chosen_city}")
    st.write(local_expert_agent(chosen_city))
    
    # ===== Get Location =====
    lat, lon = geocode_city(chosen_city)
    if lat and lon:
        st.subheader("🗺 City Map")
        show_city_map(lat, lon, chosen_city)
        
        # ===== Weather =====
        st.subheader("☀ 7-Day Weather Forecast")
        weather_data = get_weather_forecast(lat, lon)
        st.table(weather_data)
    
    # ===== Itinerary =====
    st.subheader("📝 Suggested Itinerary")
    itinerary = trip_planner_agent(chosen_city)
    st.table(itinerary)
    
    # ===== Budget =====
    st.subheader("💰 Budget Breakdown")
    budget = budget_manager_agent(budget_inr, days)
    st.write(budget)
    
    # ===== Hotels =====
    st.subheader("🏨 Hotel Recommendations")
    hotels = get_hotels(chosen_city)
    st.table(hotels)
    
    # ===== Flights =====
    st.subheader("🛫 Flight Options")
    flights = flight_price_agent(departure_city_code, chosen_city[:3].upper())
    st.write(flights)
    
    # ===== Chatbot Refinement =====
    st.subheader("💬 Chat with NavMind AI")
    user_prompt = st.text_input("Ask me to refine your itinerary:")
    if st.button("Refine"):
        chatbot_response = chatbot_agent(user_prompt)
        st.write(chatbot_response)
