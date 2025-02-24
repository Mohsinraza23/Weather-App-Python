import streamlit as st
import requests
from datetime import datetime
from typing import Dict, Any, Optional, TypedDict, Union

# Type definitions
class WeatherParams(TypedDict):
    key: str
    q: str
    days: int
    aqi: str

# Configure page
st.set_page_config(
    page_title="Weather App",
    page_icon="🌤️",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #00B4DB, #0083B0);
    }
    .weather-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        color: white;
        transition: transform 0.3s ease;
    }
    .weather-card:hover {
        transform: translateY(-5px);
    }
    .metric {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_KEY: str = "20719b81a7fe4c9380575055252402"
BASE_URL: str = "http://api.weatherapi.com/v1"

def get_weather_data(city: str) -> Optional[Dict[str, Any]]:
    """
    Fetch weather data for a given city
    """
    try:
        # Define params with correct types
        params: Dict[str, Union[str, int]] = {
            "key": API_KEY,
            "q": city,
            "days": 3,
            "aqi": "yes"
        }
        
        response = requests.get(
            f"{BASE_URL}/forecast.json",
            params=params,
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        return None
        
    except requests.RequestException as e:
        st.error(f"Failed to fetch weather data: {str(e)}")
        return None

def main() -> None:
    st.title("🌤️ Weather App")
    
    # City input
    city: str = st.text_input(
        "Enter City Name:",
        value="London",
        placeholder="Enter city name...",
        help="Type a city name and press Enter"
    )
    
    if city:
        weather_data = get_weather_data(city)
        
        if weather_data:
            current = weather_data['current']
            location = weather_data['location']
            forecast = weather_data['forecast']['forecastday']
            
            # Main weather display
            st.markdown(
                f"""
                <div class='weather-card'>
                    <h2 style='text-align: center;'>{location['name']}, {location['country']}</h2>
                    <div style='display: flex; align-items: center; justify-content: center;'>
                        <img src='https:{current['condition']['icon']}' 
                             style='width: 64px; height: 64px;'>
                        <div class='metric'>{current['temp_c']}°C</div>
                    </div>
                    <p style='text-align: center;'>{current['condition']['text']}</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Weather details in columns
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown(
                    f"""
                    <div class='weather-card'>
                        <h3>Temperature</h3>
                        <div class='metric'>{current['temp_c']}°C</div>
                        <p style='text-align: center;'>Feels like: {current['feelslike_c']}°C</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
            with col2:
                st.markdown(
                    f"""
                    <div class='weather-card'>
                        <h3>Wind</h3>
                        <div class='metric'>{current['wind_kph']} km/h</div>
                        <p style='text-align: center;'>Direction: {current['wind_dir']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
            with col3:
                st.markdown(
                    f"""
                    <div class='weather-card'>
                        <h3>Conditions</h3>
                        <div class='metric'>{current['humidity']}%</div>
                        <p style='text-align: center;'>Humidity</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            # Forecast
            st.subheader("3-Day Forecast")
            forecast_cols = st.columns(3)
            
            for i, day in enumerate(forecast):
                with forecast_cols[i]:
                    date = datetime.strptime(day['date'], '%Y-%m-%d').strftime('%A')
                    st.markdown(
                        f"""
                        <div class='weather-card'>
                            <h3 style='text-align: center;'>{date}</h3>
                            <div style='text-align: center;'>
                                <img src='https:{day['day']['condition']['icon']}' 
                                     style='width: 64px; height: 64px;'>
                            </div>
                            <div class='metric'>{day['day']['maxtemp_c']}°C</div>
                            <p style='text-align: center;'>{day['day']['condition']['text']}</p>
                            <p style='text-align: center;'>Rain: {day['day']['daily_chance_of_rain']}%</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            
            # Air Quality
            if 'air_quality' in current:
                st.subheader("Air Quality")
                aqi = current['air_quality']['us-epa-index']
                aqi_labels = {
                    1: ("Good", "#00E400"),
                    2: ("Moderate", "#FFFF00"),
                    3: ("Unhealthy for Sensitive Groups", "#FF7E00"),
                    4: ("Unhealthy", "#FF0000"),
                    5: ("Very Unhealthy", "#8F3F97"),
                    6: ("Hazardous", "#7E0023")
                }
                
                label, color = aqi_labels.get(aqi, ("Unknown", "#FFFFFF"))
                
                st.markdown(
                    f"""
                    <div class='weather-card'>
                        <h3 style='text-align: center; color: {color};'>{label}</h3>
                        <div style='display: flex; justify-content: space-around;'>
                            <div>
                                <p>PM2.5</p>
                                <div class='metric'>{current['air_quality']['pm2_5']:.1f}</div>
                            </div>
                            <div>
                                <p>PM10</p>
                                <div class='metric'>{current['air_quality']['pm10']:.1f}</div>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        else:
            st.error("City not found. Please check the spelling and try again.")

if __name__ == "__main__":
    main()