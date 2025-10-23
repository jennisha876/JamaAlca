# weather_fetcher.py

import requests
try:
    from plyer import gps
    USE_PLYER = True
except ImportError:
    USE_PLYER = False

class WeatherFetcher:
    def __init__(self):
        self.latitude = None
        self.longitude = None

    # Map weather codes to human-friendly conditions
    WEATHER_MAP = {
        0: "Clear",
        1: "Mainly Clear",
        2: "Partly Cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Fog",
        51: "Light Drizzle",
        53: "Moderate Drizzle",
        55: "Dense Drizzle",
        61: "Light Rain",
        63: "Moderate Rain",
        65: "Heavy Rain",
        71: "Light Snow",
        73: "Moderate Snow",
        75: "Heavy Snow",
        95: "Thunderstorm",
    }

    # Try to get GPS coordinates (mobile or laptop with GPS)
    def _get_gps_location(self):
        if not USE_PLYER:
            return None, None

        lat_lon = {"lat": None, "lon": None}

        def on_location(**kwargs):
            lat_lon["lat"] = kwargs.get("lat")
            lat_lon["lon"] = kwargs.get("lon")
            print(f"[GPS] Lat: {lat_lon['lat']} Lon: {lat_lon['lon']}")

        try:
            gps.configure(on_location=on_location)
            gps.start()
            import time
            time.sleep(5)  # wait briefly for GPS fix
            gps.stop()
        except Exception as e:
            print("[GPS Error]", e)

        return lat_lon["lat"], lat_lon["lon"]

    # Fallback: get rough location from IP
    def _get_ip_location(self):
        try:
            response = requests.get("http://ip-api.com/json/")
            data = response.json()
            return data["lat"], data["lon"]
        except Exception as e:
            print("[IP Location Error]", e)
            return None, None

    # Public method to get coordinates
    def get_coordinates(self):
        # Try GPS if available
        lat, lon = self._get_gps_location()

        if not lat or not lon:
            print("[INFO] Falling back to IP location...")
            lat, lon = self._get_ip_location()

        self.latitude = lat
        self.longitude = lon
        return lat, lon

    # Fetch real weather from Open-Meteo
    def get_weather_forecast(self, days=7):
        if not self.latitude or not self.longitude:
            self.get_coordinates()

        if not self.latitude or not self.longitude:
            raise ValueError("Unable to determine coordinates for weather")

        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "daily": ",".join([
                "temperature_2m_max",
                "temperature_2m_min",
                "precipitation_sum",
                "precipitation_probability_max",
                "windspeed_10m_max",
                "relative_humidity_2m_max",
                "weathercode"
            ]),
            "timezone": "auto"
        }
        r = requests.get(url, params=params)
        data = r.json()

        days_list = data["daily"]["time"]
        t_max = data["daily"]["temperature_2m_max"]
        t_min = data["daily"]["temperature_2m_min"]
        rain_mm = data["daily"]["precipitation_sum"]
        rain_chance = data["daily"]["precipitation_probability_max"]
        wind_speed = data["daily"]["windspeed_10m_max"]
        humidity = data["daily"]["relative_humidity_2m_max"]
        w_codes = data["daily"]["weathercode"]

        forecast_list = []
        for i in range(len(days_list)):
            forecast_list.append({
                "day": days_list[i],
                "temp_max": f"{t_max[i]}°C",
                "temp_min": f"{t_min[i]}°C",
                "rain_mm": f"{rain_mm[i]} mm",
                "rain_chance": f"{rain_chance[i]}%",
                "wind_speed": f"{wind_speed[i]} km/h",
                "humidity": f"{humidity[i]}%",
                "condition": self.WEATHER_MAP.get(w_codes[i], "Unknown")
            })

        return forecast_list


if __name__ == "__main__":
    wf = WeatherFetcher()
    coords = wf.get_coordinates()
    print("[Test] Coordinates:", coords)
    forecast = wf.get_weather_forecast()
    for day in forecast:
        print(day)