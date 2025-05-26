import Constants
import requests

#Hava durumu için kullandığımız fonksiyon.
def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={Constants.OPEN_WEATHER_API_KEY}&lang=tr&units=metric"
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            desc = data["weather"][0]["description"]
            temp = data["main"]["temp"]
            return f"{city} için hava durumu: {desc}, sıcaklık {temp} derece."
        else:
            return f"{city} için hava durumu alınamadı."
    except:
        return "Hava durumu servisine erişilemiyor."