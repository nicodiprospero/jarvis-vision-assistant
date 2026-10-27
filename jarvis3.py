import os
import cv2
from PIL import Image
from io import BytesIO
import base64
import asyncio
import edge_tts
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from gpt4all import GPT4All

# ===== CAMERA =====
IP_WEBCAM_URL = os.environ.get("IP_WEBCAM_URL", "http://<phone-ip>:8080/video")  # optional, if you want phone feed
cap = cv2.VideoCapture(0)  # default PC camera; change to 1 for phone camera if connected

def capture_frame():
    ret, frame = cap.read()
    if not ret:
        return None
    img = Image.fromarray(frame)
    return img

# ===== VISION MODEL (BLIP) =====
device = "cuda" if torch.cuda.is_available() else "cpu"
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base").to(device)

def analyze_image(img):
    inputs = processor(images=img, return_tensors="pt").to(device)
    out = model.generate(**inputs)
    caption = processor.decode(out[0], skip_special_tokens=True)
    return caption

# ===== GPT4All =====
gpt_model = GPT4All("ggml-gpt4all-j-v1.3-ggjt.bin", allow_download=False)  # local model file

def ask_gpt4all(prompt):
    return gpt_model.generate(prompt, max_tokens=200)

# ===== SPEECH =====
async def speak(text):
    tts = edge_tts.Communicate(text, voice="en-US-GuyNeural")
    await tts.save("tmp.mp3")
    import os
    os.system("start /min wmplayer tmp.mp3")  # Windows-only

# ===== MAIN LOOP =====
print("Jarvis offline online. Type 'exit' to quit.\n")

while True:
    command = input("You: ")
    if command.lower() == "exit":
        break

    img = capture_frame()
    if img:
        vision_text = analyze_image(img)
    else:
        vision_text = "Cannot see anything right now."

    # Combine vision + user input for GPT
    prompt = f"User said: {command}\nVision: {vision_text}\nRespond as Jarvis with personality:"
    response = ask_gpt4all(prompt)

    print("\nJarvis:", response)
    asyncio.run(speak(response))

cap.release()