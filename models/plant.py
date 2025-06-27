import requests
from tkinter import Tk, filedialog

# Hugging Face API URL for Plant Disease Identification
API_URL = "https://router.huggingface.co/hf-inference/models/linkanjarad/mobilenet_v2_1.0_224-plant-disease-identification"
HF_token = "input your own token"

# Hardcoded token for simplicity (replace with your actual token)
headers = {
    "Authorization": "Bearer "+"HF_token",
}

def select_image():
    """Open file picker to select an image."""
    root = Tk()
    root.withdraw()  # Hide the main Tkinter window
    file_path = filedialog.askopenfilename(
        title="Select a plant image",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
    )
    return file_path

def query(filename):
    """Send image to Hugging Face API for plant disease classification."""
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers={"Content-Type": "image/jpeg", **headers}, data=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)
        return None

# Main logic
image_path = select_image()

if image_path:
    output = query(image_path)
    if output:
        print("Classification Result:", output)
else:
    print("No image selected.")
