# Services Module

This directory contains backend services that power the JamaAlca application's core features.

## Available Services

1. `predict_disease.py` - AI-powered plant disease detection
   ```python
   from services.predict_disease import predict_disease

   # Usage
   disease_name, confidence = predict_disease(image_path, crop_name)
   ```

2. `treatment_recommendation.py` - AI-driven treatment suggestions
   ```python
   from services.treatment_recommendation import get_treatment_recommendation

   # Usage
   treatment_steps = get_treatment_recommendation(disease_name)
   ```

3. `weather_fetcher.py` - Real-time weather data service
   ```python
   from services.weather_fetcher import WeatherFetcher

   # Usage
   weather = WeatherFetcher()
   forecast = weather.get_weather_forecast()
   ```

## API Integration

- Azure Custom Vision API for disease detection
- OpenAI API for treatment recommendations
- Open-Meteo API for weather data

## Error Handling

Each service includes appropriate error handling:
- Network connectivity issues
- API rate limits
- Invalid input validation

## Configuration

Required environment variables:
- `AZURE_OPENAI_ENDPOINT`
- `AZURE_OPENAI_KEY`
- `PREDICTION_KEY`
- `PROJECT_ID`