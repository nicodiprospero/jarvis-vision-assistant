import cv2
import requests
import base64
import asyncio
from io import BytesIO
from PIL import Image
import edge_tts
import os

# ===== SETTINGS =====
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
IP_WEBCAM_URL = os.environ.get("IP_WEBCAM_URL", "http://<phone-ip>:8080/video")

JARVIS_PERSONALITY = """
You are Jarvis, a witty and intelligent AI assistant.
You analyze what you see through a camera and respond with clever,
slightly sarcastic observations.
Keep answers short and conversational.
"""

# ===== CAMERA =====
cap = cv2.VideoCapture(IP_WEBCAM_URL, cv2.CAP_FFMPEG)

def capture_frame():
    ret, frame = cap.read()
    if not ret:
        return None
    frame = cv2.resize(frame, (640, 480))
    img = Image.fromarray(frame)
    buffer = BytesIO()
    img.save(buffer, format="JPEG")
    return base64.b64encode(buffer.getvalue()).decode()  

# ===== AI REQUEST =====
def ask_jarvis(prompt):
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": JARVIS_PERSONALITY},
            {"role": "user", "content": prompt}
        ]
    }

    r = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload
    )
    try:
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print("Full API response:", r.text)
        return "Failed to get AI response"

# ===== VOICE =====
async def speak(text):
    tts = edge_tts.Communicate(text, voice="en-US-GuyNeural")
    await tts.save("tmp.mp3")
    os.system("start /min wmplayer tmp.mp3")  # plays via Windows Media Player

# ===== MAIN LOOP =====
print("Jarvis online. Type your commands. Type 'exit' to quit.\n")

while True:
    command = input("You: ")
    if command.lower() == "exit":
        break

    image = capture_frame()
    if image is None:
        print("Jarvis: Cannot access camera, proceeding with text only.")
        response = ask_jarvis(command)
    else:
        response = ask_jarvis(command)

    print("Jarvis:", response)
    asyncio.run(speak(response))

cap.release()