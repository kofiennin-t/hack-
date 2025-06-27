import requests
import json

endpoint = "https://stable-diffusion-3-5-large-qbmiv.eastus2.models.ai.azure.com/images/generations:submit?api-version=2023-06-01-preview"
api_key = "GpIkSyac8XKXYY43NCXw4mbJAKDcTdV7"

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

data = {
    "prompt": "A futuristic cityscape at sunset with flying cars",
    "n": 1,
    "size": "1024x1024"
}

response = requests.post(endpoint, headers=headers, json=data)

if response.status_code == 202:
    print("✅ Submitted!")
    print("🔁 Poll this URL:", response.headers.get("operation-location"))
else:
    print("❌ Error:", response.status_code)
    print(response.text)
