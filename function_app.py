import logging
import azure.functions as func
import requests  # To make the API call
app = func.FunctionApp()

WEATHER_API_URL = "https://api.openweathermap.org/data/2.5/weather"
API_KEY = "c3658cef2223b2d212386ccd4f5c5e35"  # Replace this with your OpenWeatherMap API key
CITY = "London"  # Example city

@app.timer_trigger(schedule="0 * * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def timer_trigger(myTimer: func.TimerRequest) -> None:
    if myTimer.past_due:
        logging.info('The timer is past due!')

    logging.info('api Python timer trigger function executed.ss')

# Call the free API to fetch weather data
    try:
        response = requests.get(WEATHER_API_URL, params={"q": CITY, "appid": API_KEY, "units": "metric"})

        # Check if the response is successful
        if response.status_code == 200:
            data = response.json()
            temp = data["main"]["temp"]
            weather_desc = data["weather"][0]["description"]
            logging.info(f"Weather in {CITY}: {temp}°C, {weather_desc}")
        else:
            logging.error(f"Failed to fetch weather data. Status code: {response.status_code}")
    except Exception as e:
        logging.error(f"An error occurred while calling the weather API: {e}")
