import requests

AZURE_OPENAI_ENDPOINT = "https://aihubstarbucks3126937967.cognitiveservices.azure.com/"
AZURE_OPENAI_KEY = "CzUXl0GKZIRwS0aoZJzgapKotKKFUefg05xVIUnSsEWemH4FB6PfJQQJ99ALACfhMk5XJ3w3AAAAACOGokTd"
DEPLOYMENT_NAME = "ja-students-gpt-5-chat"

def get_treatment_recommendation(disease_name):
    url = f"{AZURE_OPENAI_ENDPOINT}openai/deployments/{DEPLOYMENT_NAME}/chat/completions?api-version=2023-05-15"
    headers = {
        "Content-Type": "application/json",
        "api-key": AZURE_OPENAI_KEY
    }
    prompt = f"Suggest safe, low-cost treatment steps for {disease_name} for smallholder farmers."
    body = {
        "messages": [
            {"role": "system", "content": "You are an agricultural expert."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 150,
        "temperature": 0.3
    }

    response = requests.post(url, headers=headers, json=body)
    data = response.json()
    if "choices" in data and data["choices"]:
        return data["choices"][0]["message"]["content"].strip()
    return "No treatment available."