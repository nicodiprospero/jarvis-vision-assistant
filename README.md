<div align="center">

# Jarvis · Vision Voice Assistant

**A desktop assistant that looks through your webcam, understands the scene and talks back, built in three iterations: cloud vision → voice conversation → fully local (no API).**

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-camera-5C3EE8?logo=opencv&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-gpt--4o--mini-412991?logo=openai&logoColor=white)
![Local AI](https://img.shields.io/badge/local-BLIP%20%2B%20GPT4All-orange)
![License](https://img.shields.io/badge/license-MIT-blue)

</div>

---

## Iterations

| Script | What it adds | Runs on |
|---|---|---|
| `jarvis.py` | Grabs a webcam frame, sends it with a prompt to **gpt-4o-mini (vision)** and speaks the answer with **edge-tts** (`en-US-GuyNeural`) in a witty "Jarvis" persona | OpenAI API |
| `jarvis2.py` | Adds **voice input** (SpeechRecognition): you talk, it looks, it answers out loud | OpenAI API |
| `jarvis3.py` | **Fully local**: scene captioning with **BLIP** (`Salesforce/blip-image-captioning-base`, CUDA if available) + local LLM with **GPT4All**. No API key, no data leaves the machine | CPU / GPU |
| `cameraserver.py` | FastAPI **MJPEG stream** of the webcam (`multipart/x-mixed-replace`) for remote viewing | local network |
| `camera_preview.py`, `camera_probe.py` | Camera checks (DroidCam / phone cameras show up as index 0 or 1) | — |

## Setup

```bash
python -m venv .venv && .venv\Scripts\activate        # macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
copy .env.example .env                                # then set OPENAI_API_KEY (jarvis.py / jarvis2.py)
```

Set the variables in your shell (or load `.env` with your tool of choice), then:

```bash
python jarvis.py         # cloud vision
python jarvis2.py        # cloud vision + voice input
python jarvis3.py        # fully local
uvicorn cameraserver:app --host 0.0.0.0 --port 8000
```

For `jarvis3.py`, download a GPT4All model file and put its filename in `GPT4All(...)` (it runs with `allow_download=False`). Model files are git-ignored.

**Phone as camera:** set `IP_WEBCAM_URL` to the stream from the IP Webcam app, or use DroidCam and pick camera index 0/1.

## What I learned

- Trading off latency, cost and privacy: the same feature as a cloud call (fast, paid, data leaves the box) and fully local (free, private, heavier on hardware).
- Keeping secrets out of code: the API key comes from the environment, never from the source.

---

<sub>Built by **Nicolas Di Prospero** · [github.com/nicodiprospero](https://github.com/nicodiprospero)</sub>
