import streamlit as st
import requests
from datetime import datetime
import plotly.graph_objects as go

# Configure page
st.set_page_config(
    page_title="Weather Vista ✨",
    page_icon="🌈",
    layout="wide"
)

# Enhanced Custom CSS with animations and modern design
st.markdown("""
<style>
    /* Modern CSS Reset and Base Styles */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }

    /* Animated Background */
    .stApp {
        background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }

    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    /* Modern Glass Card */
    .glass-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.18);
        padding: 20px;
        margin: 10px 0;
        transition: all 0.3s ease;
    }

    .glass-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
    }

    /* Modern Typography */
    .title {
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(120deg, #ffffff 0%, #e0e0e0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin: 20px 0;
    }

    .metric-value {
        font-size: 2.5rem;
        font-weight: 600;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }

    .metric-label {
        font-size: 1.2rem;
        color: rgba(255,255,255,0.9);
        margin-top: 5px;
    }

    /* Custom Input Styling */
    .stTextInput input {
        background: rgba(255, 255, 255, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 25px;
        color: white;
        padding: 15px 25px;
        font-size: 1.2rem;
        transition: all 0.3s ease;
    }

    .stTextInput input:focus {
        background: rgba(255, 255, 255, 0.15);
        border-color: rgba(255, 255, 255, 0.5);
        box-shadow: 0 0 15px rgba(255,255,255,0.2);
    }

    /* Weather Icon Container */
    .weather-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 50%;
        width: 80px;
        height: 80px;
        margin: 10px auto;
        padding: 15px;
    }

    .weather-icon img {
        width: 100%;
        height: 100%;
        object-fit: contain;
    }

    /* Forecast Cards */
    .forecast-card {
        text-align: center;
        padding: 15px;
        border-radius: 15px;
        background: rgba(255, 255, 255, 0.05);
        transition: transform 0.3s ease;
    }

    .forecast-card:hover {
        transform: scale(1.02);
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }

    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 5px;
    }

    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.3);
        border-radius: 5px;
    }

    /* Responsive Design */
    @media (max-width: 768px) {
        .title {
            font-size: 2.5rem;
        }
        .metric-value {
            font-size: 2rem;
        }
        .glass-card {
            padding: 15px;
        }
    }
</style>
""", unsafe_allow_html=True)

# WeatherAPI.com API Key
API_KEY = "20719b81a7fe4c9380575055252402"
BASE_URL = "http://api.weatherapi.com/v1"

def get_weather_data(city):
    """Get current weather and forecast data"""
    try:
        response = requests.get(
            f"{BASE_URL}/forecast.json",
            params={
                "key": API_KEY,
                "q": city,
                "days": 3,
                "aqi": "yes"
            }
        )
        return response.json() if response.status_code == 200 else None
    except Exception as e:
        st.error(f"Error fetching weather data: {e}")
        return None

def get_weather_emoji(condition_code):
    """Get appropriate emoji for weather condition"""
    condition_map = {
        1000: "☀️",  # Sunny
        1003: "🌤️",  # Partly cloudy
        1006: "☁️",  # Cloudy
        1009: "🌫️",  # Overcast
        1030: "🌫️",  # Mist
        1063: "🌧️",  # Rain
        1066: "🌨️",  # Snow
        1087: "⛈️",  # Thunder
    }
    return condition_map.get(condition_code, "🌈")

def main():
    st.markdown('<h1 class="title">Weather Vista ✨</h1>', unsafe_allow_html=True)
    
    # Stylish search bar
    city = st.text_input("", 
                        placeholder="🔍 Enter city name...",
                        help="Type a city name and press Enter")
    
    if city:
        weather_data = get_weather_data(city)
        
        if weather_data:
            current = weather_data['current']
            location = weather_data['location']
            forecast = weather_data['forecast']['forecastday']
            
            # Current Weather Display
            st.markdown(
                f"""
                <div class="glass-card">
                    <h2 style="color: white; text-align: center; font-size: 2rem;">
                        {location['name']}, {location['country']}
                    </h2>
                    <div class="weather-icon">
                        <img src="https:{current['condition']['icon']}" alt="Weather icon">
                    </div>
                    <div style="text-align: center;">
                        <div class="metric-value">{current['temp_c']}°C</div>
                        <div class="metric-label">{current['condition']['text']}</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Current Conditions Grid
            cols = st.columns(4)
            metrics = [
                ("🌡️ Feels Like", f"{current['feelslike_c']}°C"),
                ("💨 Wind", f"{current['wind_kph']} km/h"),
                ("💧 Humidity", f"{current['humidity']}%"),
                ("☀️ UV Index", str(current['uv']))
            ]
            
            for col, (label, value) in zip(cols, metrics):
                with col:
                    st.markdown(
                        f"""
                        <div class="glass-card" style="text-align: center;">
                            <div class="metric-label">{label}</div>
                            <div class="metric-value">{value}</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            
            # 3-Day Forecast
            st.markdown(
                '<h2 style="color: white; text-align: center; margin: 30px 0;">3-Day Forecast</h2>',
                unsafe_allow_html=True
            )
            
            forecast_cols = st.columns(3)
            for i, day in enumerate(forecast):
                with forecast_cols[i]:
                    date = datetime.strptime(day['date'], '%Y-%m-%d').strftime('%A')
                    st.markdown(
                        f"""
                        <div class="glass-card forecast-card">
                            <h3 style="color: white;">{date}</h3>
                            <div class="weather-icon">
                                <img src="https:{day['day']['condition']['icon']}" alt="Forecast icon">
                            </div>
                            <div class="metric-value">{day['day']['maxtemp_c']}°C</div>
                            <div class="metric-label">{day['day']['mintemp_c']}°C</div>
                            <div style="color: white; margin-top: 10px;">
                                {day['day']['condition']['text']}
                            </div>
                            <div style="color: rgba(255,255,255,0.8); margin-top: 5px;">
                                Rain: {day['day']['daily_chance_of_rain']}%
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            
            # Hourly Temperature Graph
            st.markdown(
                '<h2 style="color: white; text-align: center; margin: 30px 0;">Temperature Trend</h2>',
                unsafe_allow_html=True
            )
            
            hours = []
            temps = []
            
            for day in forecast:
                for hour in day['hour']:
                    hours.append(datetime.fromtimestamp(hour['time_epoch']))
                    temps.append(hour['temp_c'])
            
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=hours,
                y=temps,
                mode='lines+markers',
                name='Temperature',
                line=dict(
                    color='white',
                    width=3,
                    shape='spline'
                ),
                marker=dict(
                    size=8,
                    color='white',
                    line=dict(
                        color='rgba(255, 255, 255, 0.5)',
                        width=2
                    )
                ),
                fill='tonexty',
                fillcolor='rgba(255, 255, 255, 0.1)'
            ))
            
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                title={
                    'text': 'Hourly Temperature Forecast',
                    'y':0.95,
                    'x':0.5,
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'font': dict(
                        color='white',
                        size=24
                    )
                },
                xaxis=dict(
                    title='Time',
                    color='white',
                    gridcolor='rgba(255,255,255,0.1)',
                    showgrid=True
                ),
                yaxis=dict(
                    title='Temperature (°C)',
                    color='white',
                    gridcolor='rgba(255,255,255,0.1)',
                    showgrid=True
                ),
                hovermode='x unified'
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Air Quality Section
            if 'air_quality' in current:
                st.markdown(
                    '<h2 style="color: white; text-align: center; margin: 30px 0;">Air Quality</h2>',
                    unsafe_allow_html=True
                )
                
                aqi = current['air_quality']['us-epa-index']
                aqi_colors = {
                    1: "#00E400",  # Good
                    2: "#FFFF00",  # Moderate
                    3: "#FF7E00",  # Unhealthy for sensitive groups
                    4: "#FF0000",  # Unhealthy
                    5: "#8F3F97",  # Very Unhealthy
                    6: "#7E0023"   # Hazardous
                }
                
                aqi_labels = {
                    1: "Good",
                    2: "Moderate",
                    3: "Sensitive",
                    4: "Unhealthy",
                    5: "Very Unhealthy",
                    6: "Hazardous"
                }
                
                st.markdown(
                    f"""
                    <div class="glass-card" style="text-align: center;">
                        <div style="font-size: 2rem; color: {aqi_colors.get(aqi, '#ffffff')};">
                            {aqi_labels.get(aqi, "Unknown")}
                        </div>
                        <div style="display: flex; justify-content: space-around; margin-top: 20px;">
                            <div>
                                <div class="metric-label">PM2.5</div>
                                <div class="metric-value">{current['air_quality']['pm2_5']:.1f}</div>
                            </div>
                            <div>
                                <div class="metric-label">PM10</div>
                                <div class="metric-value">{current['air_quality']['pm10']:.1f}</div>
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