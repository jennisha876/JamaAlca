import requests
from config import Config

# Use configuration from config.py
AZURE_OPENAI_ENDPOINT = Config.AZURE_OPENAI_ENDPOINT
AZURE_OPENAI_KEY = Config.AZURE_OPENAI_KEY
DEPLOYMENT_NAME = Config.DEPLOYMENT_NAME

def get_treatment_recommendation(disease_name):
    try:
        if not disease_name or not disease_name.strip():
            return "No disease specified for treatment recommendation."
        
        url = f"{AZURE_OPENAI_ENDPOINT}openai/deployments/{DEPLOYMENT_NAME}/chat/completions?api-version=2023-05-15"
        headers = {
            "Content-Type": "application/json",
            "api-key": AZURE_OPENAI_KEY
        }
        prompt = f"Suggest safe, low-cost treatment steps for {disease_name} for smallholder farmers in Jamaica and even corporate farms. (NB: give a succinct and direct response)"
        body = {
            "messages": [
                {"role": "system", "content": "You are a Jamaican agricultural expert."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 150,
            "temperature": 0.3
        }

        response = requests.post(url, headers=headers, json=body, timeout=30)
        response.raise_for_status()  # Raise exception for HTTP errors
        
        data = response.json()
        if "choices" in data and data["choices"]:
            return data["choices"][0]["message"]["content"].strip()
        return "No treatment available."
        
    except requests.exceptions.Timeout:
        return "Treatment recommendation service is currently unavailable. Please try again later."
    except requests.exceptions.RequestException as e:
        print(f"Error fetching treatment recommendation: {e}")
        return "Unable to get treatment recommendation at this time."
    except Exception as e:
        print(f"Unexpected error in treatment recommendation: {e}")
        return "No treatment available."