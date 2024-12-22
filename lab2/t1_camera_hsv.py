import cv2
import sys

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Не удалось открыть камеру")
    sys.exit(-1)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Ошибка при получении кадра")
        break

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    cv2.imshow('BGR', frame)
    cv2.imshow('HSV', hsv_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
