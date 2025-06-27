import requests
import io
from PIL import Image

# API URL for the FLUX text-to-image model
API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-dev"

# Hardcoded Hugging Face token for simplicity (replace with your real token)
headers = {
    "Authorization": "Bearer hf_....",
}

def query(prompt):
    payload = {"inputs": prompt}
    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        return response.content
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)
        return None

# Main logic
prompt = input("Enter a prompt to generate an image: ")

image_bytes = query(prompt)

if image_bytes:
    image = Image.open(io.BytesIO(image_bytes))
    image.show()