import requests
from bs4 import BeautifulSoup
from datetime import datetime

api_key="https://home.openweathermap.org/ ---> api key"
city=input("Enter city name:")

url = f"http://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}&units=metric"

try:
    response = requests.get(url)
    data=response.json()

    if data["cod"] != "200":
        print(f"Hata:  {data['message']}")
    else:
        print(f"\n5 günlük hava durumu - {city}\n"+"-"*40)


        forecasts = {}
        for item in data['list']:
            date = datetime.fromtimestamp(item['dt']).strftime('%d.%m.%Y')
            if date not in forecasts:
                forecasts[date] = []
            forecasts[date].append(item)
        for date, items in forecasts.items():
                    avg_temp = sum(item['main']['temp'] for item in items) / len(items)
                    weather_desc = items[0]['weather'][0]['description']

                    print(f"{date}:")
                    print(f"  → Weather: {weather_desc.capitalize()}")
                    print(f"  → Temp: {avg_temp:.1f}°C")
                    print(f"  → Humidity: {items[0]['main']['humidity']}%")
                    print(f"  → Wind: {items[0]['wind']['speed']} km/sa\n")
except Exception as e:
    print(f"Hata oluştu: {e}")