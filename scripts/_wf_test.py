import sys, os
# Ensure repo root is on sys.path so we can import local modules when running
# from the scripts/ directory.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from weather_fetcher import WeatherFetcher

wf = WeatherFetcher()
print('coords->', wf.get_coordinates())
try:
    f = wf.get_weather_forecast(days=3)
    print('forecast len', len(f))
    for day in f:
        print(day)
except Exception as e:
    print('forecast error', e)
