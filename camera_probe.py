import cv2

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)  # Try 0 or 1

if not cap.isOpened():
    print("Cannot open camera")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break

    cv2.imshow('Test Camera', frame)
    if cv2.waitKey(1) == 27:  # Press ESC to quit
        break

cap.release()
cv2.destroyAllWindows()