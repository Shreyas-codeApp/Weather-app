import streamlit as st
import requests,datetime
url = "https://api.open-meteo.com/v1/forecast"
st.title("The Weather App!")
coordinates = [
    {"location": "Mumbai", "latitude": 19.0760, "longitude": 72.8777},
    {"location": "Pune", "latitude": 18.5204, "longitude": 73.8567},
    {"location": "Delhi", "latitude": 28.7041, "longitude": 77.1025},
    {"location": "Colombo", "latitude": 6.9271, "longitude": 79.8612},
    {"location": "Berlin", "latitude": 52.5200, "longitude": 13.4050},
    {"location": "Tokyo", "latitude": 35.6762, "longitude": 139.6503},
    {"location": "London", "latitude": 51.5072, "longitude": -0.1276},
    {"location": "Sydney", "latitude": -33.8688, "longitude": 151.2093},
    {"location": "Brisbane", "latitude": -27.4698, "longitude": 153.0251},
    {"location": "New York", "latitude": 40.7128, "longitude": -74.0060},
    {"location": "Paris", "latitude": 48.8566, "longitude": 2.3522},
    {"location": "Dubai", "latitude": 25.276987, "longitude": 55.296249},
    {"location": "Singapore", "latitude": 1.3521, "longitude": 103.8198},
    {"location": "Cape Town", "latitude": -33.9249, "longitude": 18.4241},
    {"location": "Rome", "latitude": 41.9028, "longitude": 12.4964}
]

locations = [place["location"] for place in coordinates]
selected_place = st.selectbox("Select a city: ", locations)
params = {
    "latitude": "",
    "longitude": "",
    "hourly": "temperature_2m,relative_humidity_2m"
}
for place in coordinates:
    if place["location"] == selected_place:
        params["latitude"] = place["latitude"]
        params["longitude"] = place["longitude"]




current_time = datetime.datetime.now()
def get_weather():
    response = requests.get(url, params=params).json()
    timestamps = response["hourly"]["time"]
    temperature = response["hourly"]["temperature_2m"]
    humidity = response["hourly"]["relative_humidity_2m"]
    current_hour = current_time.strftime("%H")
    current_date = current_time.strftime("%d")
    #2025-09-08T12:00
    for i in timestamps:
        if i[11:13] == current_hour and i[8:10] == current_date:
            element_index = timestamps.index(i)
    return temperature[element_index],humidity[element_index],temperature,humidity,timestamps

current_temp,current_hum,temperature,humidity,timestamp = get_weather()
if st.button("Get weather data!"):
    current_time = datetime.datetime.now()
    st.metric(label = "Time of your machine:",value = current_time.strftime("%X"))
    st.metric(label = "Gepgraphical coordinates:",value = f"Latitude: {params['latitude']}, Longitude: {params['longitude']} ")
    st.metric(label = "Temperature:",value = f"{current_temp}°C")
    st.metric(label="Humidity:",value = f"{current_hum}%")
option = st.selectbox("Pick one: ",["Temperature","Humidity"])
temperature_graph = []
humidity_graph = []
if st.checkbox("Show graph"):
    if option == "Temperature":
        for i in timestamp:
            if i[8:10] == current_time.strftime("%d"):
                    temperature_graph.append(temperature[timestamp.index(i)])
        st.write("Temperature graph for today")
        st.bar_chart(temperature_graph)           
    if option == "Humidity":
        for i in timestamp:
            if i[8:10] == current_time.strftime("%d"):
                    humidity_graph.append(humidity[timestamp.index(i)])    
        st.write("Humidity graph for today")        
        st.bar_chart(humidity_graph)

    