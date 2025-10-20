from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
import os

# ==== CONFIG ====
ENDPOINT = "https://southcentralus.api.cognitive.microsoft.com/"
PREDICTION_KEY = "90ca8ee92dd24300a83bacd04f5ad06c"
PROJECT_ID = "2c93ae6d-150e-429a-ad9c-d2b605d02e65"
PUBLISHED_NAME = "Plant Disease Detector"

# ==== CLIENT ====
predictor = CustomVisionPredictionClient(PREDICTION_KEY, endpoint=ENDPOINT)

def predict_disease(image_path):
    with open(image_path, "rb") as image_data:
        results = predictor.classify_image(
            PROJECT_ID,
            PUBLISHED_NAME,
            image_data
        )

    top_result = max(results.predictions, key=lambda p: p.probability)

    disease_name = top_result.tag_name
    confidence = round(top_result.probability * 100, 2)

    return disease_name, confidence