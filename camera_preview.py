import cv2

cap = cv2.VideoCapture(0)  # DroidCam usually becomes camera 0 or 1

while True:
    ret, frame = cap.read()

    if not ret:
        print("Camera not detected")
        break

    cv2.imshow("Jarvis Camera", frame)

    if cv2.waitKey(1) == 27:
        break

cap.release()
cv2.destroyAllWindows()