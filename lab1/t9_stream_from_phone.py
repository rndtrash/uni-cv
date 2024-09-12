import cv2

video_url = "http://192.168.1.67:8080/video"

cap = cv2.VideoCapture(video_url)

if not cap.isOpened():
    print("Ошибка открытия видеопотока с телефона")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Ошибка при получении кадра")
        break

    cv2.imshow('Видео с камеры телефона', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
