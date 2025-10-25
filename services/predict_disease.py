from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials
import os
from config import Config

# Use configuration from config.py
ENDPOINT = Config.AZURE_VISION_ENDPOINT
PREDICTION_KEY = Config.AZURE_VISION_PREDICTION_KEY
PROJECT_ID = Config.AZURE_VISION_PROJECT_ID
PUBLISHED_NAME = Config.AZURE_VISION_PUBLISHED_NAME

# Create credentials object with the prediction key
credentials = ApiKeyCredentials(in_headers={"Prediction-key": PREDICTION_KEY})

# Pass endpoint first, then credentials object
predictor = CustomVisionPredictionClient(ENDPOINT, credentials)

def predict_disease(image_path, crop_name):
    try:
        # Validate inputs
        if not image_path or not os.path.exists(image_path):
            return "Image file not found", 0.0
        
        if not crop_name or crop_name.strip() == "":
            return "Crop name not specified", 0.0
        
        # Check if file is a valid image
        if not image_path.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            return "Invalid image format", 0.0
        
        # You can use crop_name to select the right Azure model OR filter results
        with open(image_path, "rb") as image_data:
            results = predictor.classify_image(
                PROJECT_ID,
                PUBLISHED_NAME,
                image_data
            )

        if not results.predictions:
            return "No predictions available", 0.0

        # Filter predictions for that crop
        crop_results = [p for p in results.predictions if p.tag_name.lower().startswith(crop_name.lower())]
        top_result = max(crop_results, key=lambda p: p.probability) if crop_results else max(results.predictions, key=lambda p: p.probability)

        disease_name = top_result.tag_name
        confidence = round(top_result.probability * 100, 2)

        return disease_name, confidence
        
    except FileNotFoundError:
        return "Image file not found", 0.0
    except PermissionError:
        return "Permission denied accessing image file", 0.0
    except Exception as e:
        print(f"Error in disease prediction: {e}")
        return "Error analyzing image", 0.0