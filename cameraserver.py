import cv2
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

cap = cv2.VideoCapture(0)

def generate():

    while True:

        ret, frame = cap.read()

        if not ret:
            continue

        _, buffer = cv2.imencode(".jpg", frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.get("/")
def video():

    return StreamingResponse(
        generate(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )