import os
import cv2
import base64
import requests
import speech_recognition as sr
import asyncio
import edge_tts
from io import BytesIO
from PIL import Image

# ===== SETTINGS =====

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

JARVIS_PERSONALITY = """
You are Jarvis, a witty and intelligent AI assistant.
You analyze what you see through a camera and respond with clever,
slightly sarcastic observations.
Keep answers short and conversational.
"""

# ===== VOICE =====

async def speak(text):
    tts = edge_tts.Communicate(text, voice="en-US-GuyNeural")
    await tts.run()

# ===== CAMERA =====

cap = cv2.VideoCapture(0)

def capture_frame():

    ret, frame = cap.read()

    if not ret:
        return None

    frame = cv2.resize(frame, (640,480))

    img = Image.fromarray(frame)
    buffer = BytesIO()
    img.save(buffer, format="JPEG")

    return base64.b64encode(buffer.getvalue()).decode()

# ===== AI REQUEST =====

def ask_jarvis(prompt, image_b64):

    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": JARVIS_PERSONALITY},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{image_b64}"
                        }
                    }
                ]
            }
        ]
    }

    r = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers=headers,
        json=payload
    )

    return r.json()["choices"][0]["message"]["content"]

# ===== SPEECH RECOGNITION =====

recognizer = sr.Recognizer()

def listen():

    with sr.Microphone() as source:

        print("Listening...")
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        return text.lower()
    except:
        return ""

# ===== MAIN LOOP =====

print("Jarvis online.")

while True:

    speech = listen()

    if "jarvis" in speech:

        print("Wake word detected.")

        print("What do you want?")

        command = listen()

        print("You:", command)

        image = capture_frame()

        if image is None:
            response = "I cannot access the camera."
        else:
            response = ask_jarvis(command, image)

        print("Jarvis:", response)

        asyncio.run(speak(response))