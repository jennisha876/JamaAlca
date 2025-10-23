from azure.cognitiveservices.vision.customvision.prediction import CustomVisionPredictionClient
from msrest.authentication import ApiKeyCredentials

ENDPOINT = "https://southcentralus.api.cognitive.microsoft.com/"
PREDICTION_KEY = "90ca8ee92dd24300a83bacd04f5ad06c"
PROJECT_ID = "2c93ae6d-150e-429a-ad9c-d2b605d02e65"
PUBLISHED_NAME = "JamaAlca Vision"

# Create credentials object with the prediction key
credentials = ApiKeyCredentials(in_headers={"Prediction-key": PREDICTION_KEY})

# Pass endpoint first, then credentials object
predictor = CustomVisionPredictionClient(ENDPOINT, credentials)

def predict_disease(image_path, crop_name):
    # You can use crop_name to select the right Azure model OR filter results
    with open(image_path, "rb") as image_data:
        results = predictor.classify_image(
            PROJECT_ID,
            PUBLISHED_NAME,
            image_data
        )

    # Filter predictions for that crop
    crop_results = [p for p in results.predictions if p.tag_name.lower().startswith(crop_name.lower())]
    top_result = max(crop_results, key=lambda p: p.probability) if crop_results else max(results.predictions, key=lambda p: p.probability)

    disease_name = top_result.tag_name
    confidence = round(top_result.probability * 100, 2)

    return disease_name, confidence