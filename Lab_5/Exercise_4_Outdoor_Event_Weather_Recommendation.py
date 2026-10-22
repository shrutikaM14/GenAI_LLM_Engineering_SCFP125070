from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser, StrOutputParser
from pydantic import BaseModel, Field
import os
import requests

load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    api_key=os.environ["GROQ_API_KEY"]
)


# Step 1: Structured output schema
class EventData(BaseModel):
    event_type: str = Field(
        description="The type of event being planned"
    )
    event_date: str = Field(
        description="The date of the event"
    )
    location: str = Field(
        description="The location where the event will take place"
    )
    indoor_outdoor_preference: str = Field(
        description="Whether the event is preferred to be indoors or outdoors"
    )


parser_step1 = PydanticOutputParser(
    pydantic_object=EventData
)


# Step 1: PromptTemplate
event_prompt = PromptTemplate.from_template(
    """
Extract the event type, event date, location, and indoor/outdoor
preference from the following event description.

Event Description:
{event_description_text}

{format_instructions}
"""
).partial(
    format_instructions=parser_step1.get_format_instructions()
)


# Step 2: Weather structured output schema
class WeatherData(BaseModel):
    temperature: str = Field(
        description="The forecast temperature"
    )
    precipitation_chance: str = Field(
        description="The chance of precipitation"
    )
    conditions: str = Field(
        description="The weather conditions"
    )


parser_step2 = PydanticOutputParser(
    pydantic_object=WeatherData
)


# Take event description from user
event_description_text = input(
    "Enter outdoor event description: "
)


# Step 1
step1_input = event_prompt.invoke({
    "event_description_text": event_description_text
})

step1_response = llm.invoke(step1_input)

event_data = parser_step1.invoke(step1_response)


# Step 2: Get weather information
# Using Open-Meteo geocoding API to find the location
geocoding_url = "https://geocoding-api.open-meteo.com/v1/search"

geocoding_response = requests.get(
    geocoding_url,
    params={
        "name": event_data.location,
        "count": 1,
        "language": "en",
        "format": "json"
    }
)

geocoding_data = geocoding_response.json()

if "results" not in geocoding_data:
    print("\nCould not find the event location.")
    exit()

latitude = geocoding_data["results"][0]["latitude"]
longitude = geocoding_data["results"][0]["longitude"]


weather_url = "https://api.open-meteo.com/v1/forecast"

weather_response = requests.get(
    weather_url,
    params={
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max,precipitation_probability_max,weather_code",
        "timezone": "auto"
    }
)

weather_data_raw = weather_response.json()


# Find the requested date in the forecast
forecast_dates = weather_data_raw["daily"]["time"]

if event_data.event_date not in forecast_dates:
    print("\nWeather forecast is not available for the requested date.")
    exit()

date_index = forecast_dates.index(event_data.event_date)

temperature = weather_data_raw["daily"]["temperature_2m_max"][date_index]
precipitation = weather_data_raw["daily"]["precipitation_probability_max"][date_index]
weather_code = weather_data_raw["daily"]["weather_code"][date_index]


# Convert weather code into simple conditions
if weather_code == 0:
    conditions = "Clear sky"
elif weather_code in [1, 2, 3]:
    conditions = "Partly cloudy or cloudy"
elif weather_code in [51, 53, 55, 56, 57]:
    conditions = "Drizzle"
elif weather_code in [61, 63, 65, 66, 67]:
    conditions = "Rain"
elif weather_code in [71, 73, 75, 77]:
    conditions = "Snow"
elif weather_code in [80, 81, 82]:
    conditions = "Rain showers"
elif weather_code in [95, 96, 99]:
    conditions = "Thunderstorm"
else:
    conditions = "Unknown"


# Normalize weather information into structured output
weather_structured = WeatherData(
    temperature=f"{temperature}°C",
    precipitation_chance=f"{precipitation}%",
    conditions=conditions
)


# Step 3: ChatPromptTemplate
recommendation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an event planning assistant."
        ),
        (
            "user",
            """
Give a weather-adjusted recommendation for the event using only
the structured event data and structured weather data below.

Event Type: {event_type}
Event Date: {event_date}
Location: {location}
Indoor/Outdoor Preference: {preference}

Temperature: {temperature}
Precipitation Chance: {precipitation_chance}
Conditions: {conditions}

Recommend whether the event should proceed outdoors,
move indoors, or take weather precautions.

Explain the recommendation briefly.
Do not use information outside the provided structured data.
"""
        )
    ]
)


str_parser = StrOutputParser()


# Step 3
step3_input = recommendation_prompt.invoke({
    "event_type": event_data.event_type,
    "event_date": event_data.event_date,
    "location": event_data.location,
    "preference": event_data.indoor_outdoor_preference,
    "temperature": weather_structured.temperature,
    "precipitation_chance": weather_structured.precipitation_chance,
    "conditions": weather_structured.conditions
})

step3_response = llm.invoke(step3_input)

recommendation = str_parser.invoke(step3_response)


# Display results
print("\nStep 1 - Structured Event Data:")
print(event_data)

print("\nStep 2 - Structured Weather Data:")
print(weather_structured)

print("\nStep 3 - Weather-Adjusted Recommendation:")
print(recommendation)