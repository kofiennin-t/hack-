import requests
from tkinter import Tk, filedialog

# Hugging Face API URL for NSFW detection
API_URL = "https://router.huggingface.co/hf-inference/models/Falconsai/nsfw_image_detection"

# Hardcoded token — replace with your actual token
HF_TOKEN = "Change to your Token"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
}

def select_image():
    """Open file picker to select an image."""
    root = Tk()
    root.withdraw()  # Hide the main Tkinter window
    file_path = filedialog.askopenfilename(
        title="Select an image",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png *.bmp *.gif")]
    )
    return file_path

def query(filename):
    """Send image to Hugging Face API for NSFW detection."""
    with open(filename, "rb") as f:
        data = f.read()
    response = requests.post(API_URL, headers={"Content-Type": "image/jpeg", **headers}, data=data)
    return response.json()

# Main logic
image_path = select_image()
if image_path:
    output = query(image_path)
    print(output)
else:
    print("No image selected.")
