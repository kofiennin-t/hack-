import requests

# API URL for Zephyr 7B Chat Model
API_URL = "https://router.huggingface.co/hf-inference/models/HuggingFaceH4/zephyr-7b-beta/v1/chat/completions"
HF_Token ="Input your Token" 
# Hardcoded token for simplicity (replace with your real token)
headers = {
    "Authorization": "Bearer "+"HF_Token",
      "Content-Type": "application/json"
}

def query(messages):
    payload = {
        "model": "HuggingFaceH4/zephyr-7b-beta",
        "messages": messages
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Main logic
user_input = input("Enter your prompt: ")

messages = [
    {"role": "user", "content": user_input}
]

response = query(messages)

# Print assistant's reply
print("Assistant:", response["choices"][0]["message"]["content"])
