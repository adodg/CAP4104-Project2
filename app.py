import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
from datetime import date
import matplotlib.dates as mdates

# Fetch Open Meteo data using the provided zip code
def fetch_weather(zipcode):
    r = requests.get("https://geocoding-api.open-meteo.com/v1/search?name=" + zipcode)
    geo = r.json()

    # Show error if we don't get results from Meteo
    if not geo or 'results' not in geo or len(geo['results']) == 0:
        return None, None, None

    # Get the first result's lat and long
    lat = geo['results'][0]['latitude']
    lon = geo['results'][0]['longitude']

    # Call back out with the lat and long and fetch our metrics
    weather_r = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m&timezone=auto")
    weather = weather_r.json()

    return weather, lat, lon

# Create the pandas dataframe and map to our wanted syntax, and convert metric to imperial where needed
def make_df(weather, unit):
    df = pd.DataFrame({
        'time': pd.to_datetime(weather['hourly']['time']),
        'temp': weather['hourly']['temperature_2m'],
        'humidity': weather['hourly']['relative_humidity_2m'],
        'wind': weather['hourly']['wind_speed_10m']
    })

    if unit == 'Fahrenheit':
        df['temp'] = df['temp'] * 9 / 5 + 32

    df['wind_mph'] = df['wind'] * 2.237
    return df

# Format the date output to show in hh:mm am/pm syntax, configurable to an nth hour (using every hour for now since switching to wide container)
def format_time_axis(ax, show_every_nth_hour=1):
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=show_every_nth_hour))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%I:%M%p'))
    ax.tick_params(axis='x', rotation=45)

def main():
    # Create the basic streamlit setup w/ title, headerr, etc
    st.set_page_config(page_title="Weather App", layout="wide")
    st.title("Weather App")

    st.sidebar.header("User Input")
    zipcode = st.sidebar.text_input("Enter ZIP Code:")
    unit = st.sidebar.radio("Temperature Unit:", ['Fahrenheit', 'Celsius'])

    show_temp = st.sidebar.checkbox("Temperature", value=True)
    show_humidity = st.sidebar.checkbox("Humidity")
    show_wind = st.sidebar.checkbox("Wind Speed")

    plt.style.use('dark_background')

    # Fetch data on click, then store to streamlit session
    if st.sidebar.button("Get Weather Data"):
        if zipcode:
            weather, lat, lon = fetch_weather(zipcode)
            if weather is None or lat is None or lon is None:
                st.sidebar.error("Error fetching weather data")
                return
            st.session_state.weather = weather
            st.session_state.lat = lat
            st.session_state.lon = lon
            st.sidebar.success("Data loaded!")

    # Clear streamlit data from session
    if st.sidebar.button("Clear"):
        del st.session_state.weather
        st.rerun()

    # Display if session state exists
    if hasattr(st.session_state, 'weather'):
        df = make_df(st.session_state.weather, unit)
        today = df[df['time'].dt.date == date.today()]

        tabs = []
        if show_temp:
            tabs.append("Temperature")
        if show_humidity:
            tabs.append("Humidity")
        if show_wind:
            tabs.append("Wind")

        # Always append data tab
        tabs.append("Data")

        tab_objects = st.tabs(tabs)

        # Enumerate over tabs that have data (and data tab)
        # Using matplotlib as the default streamlit charts don't provide enough customization for what I was trying to display
        for i, tab_name in enumerate(tabs):
            with tab_objects[i]:
                if tab_name == "Temperature":
                    st.header("Temperature")
                    fig, ax = plt.subplots(figsize=(16, 5))
                    ax.plot(today['time'], today['temp'])
                    ax.set_title('Today\'s Temperature')
                    ax.set_ylabel(f"Temperature ({unit[0]})")
                    format_time_axis(ax)
                    plt.tight_layout()
                    st.pyplot(fig)

                    daily = df.groupby(df['time'].dt.date)['temp'].agg(['min', 'max'])
                    fig, ax = plt.subplots(figsize=(16, 5))
                    ax.plot(daily.index, daily['max'], 'r-', label='High')
                    ax.plot(daily.index, daily['min'], 'b-', label='Low')
                    ax.set_title('7-day Temps')
                    ax.legend()
                    ax.tick_params(axis='x', rotation=45)
                    ax.set_ylabel(f"Temperature ({unit[0]})")
                    plt.tight_layout()
                    st.pyplot(fig)

                elif tab_name == "Humidity":
                    st.header("Humidity")

                    fig, ax = plt.subplots(figsize=(16, 5))
                    ax.plot(today['time'], today['humidity'])
                    ax.set_title('Today\'s Humidity')
                    ax.set_ylabel("Humidity %")
                    format_time_axis(ax)
                    plt.tight_layout()
                    st.pyplot(fig)

                    daily_hum = df.groupby(df['time'].dt.date)['humidity'].mean()
                    fig, ax = plt.subplots(figsize=(16, 5))
                    ax.plot(daily_hum.index, daily_hum.values)
                    ax.set_title('7-day Humidity')
                    ax.tick_params(axis='x', rotation=45)
                    ax.set_ylabel("Humidity %")
                    plt.tight_layout()
                    st.pyplot(fig)

                elif tab_name == "Wind":
                    st.header("Wind")

                    fig, ax = plt.subplots(figsize=(16, 5))
                    ax.plot(today['time'], today['wind_mph'])
                    ax.set_title('Today\'s Wind')
                    ax.set_ylabel("Wind (mph)")
                    format_time_axis(ax)
                    plt.tight_layout()
                    st.pyplot(fig)

                    daily_wind = df.groupby(df['time'].dt.date)['wind_mph'].mean()
                    fig, ax = plt.subplots(figsize=(16, 5))
                    ax.plot(daily_wind.index, daily_wind.values)
                    ax.set_title('7-day Wind')
                    ax.tick_params(axis='x', rotation=45)
                    ax.set_ylabel("Wind (mph)")
                    plt.tight_layout()
                    st.pyplot(fig)

                elif tab_name == "Data":
                    st.header("Data")

                    st.write("Records:", len(df))
                    st.write("Location:", st.session_state.lat, st.session_state.lon)

                    map_df = pd.DataFrame({'lat': [st.session_state.lat], 'lon': [st.session_state.lon]})
                    st.map(map_df)

                    st.dataframe(df)
    else:
        st.write("Enter zip code on the left sidebar, then press \"Get Weather Data\" to fetch weather data")


if __name__ == "__main__":
    main()