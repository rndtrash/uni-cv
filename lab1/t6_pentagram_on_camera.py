import math

import cv2

# открываем камеру, где 0 камера по умолчанию
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Ошибка открытия камеры")
    exit()

while True:
    # захват кадра пока работаем
    ret, frame = cap.read()

    if not ret:
        print("Не удалось получить кадр с камеры")
        break

    # Получаем размеры кадра
    height, width = frame.shape[:2]

    # Считаем центр изображения
    center_x, center_y = width // 2, height // 2

    for i in range(5):
        length = 50
        angle = math.pi / 2 + i / 5.0 * 2.0 * math.pi
        xyFirst = (int(math.cos(angle) * length + center_x), int(center_y - math.sin(angle) * length))

        # Пятиугольник
        angleNext = math.pi / 2 + (i + 1) / 5.0 * 2.0 * math.pi
        xySecond = (int(math.cos(angleNext) * length + center_x), int(center_y - math.sin(angleNext) * length))
        # горизонтальная линия в 2 пикселя красная
        cv2.line(frame, xyFirst, xySecond, (0, 0, 255), 2)

        # Пентаграма
        angleLeft = math.pi / 2 + (i + 2) / 5.0 * 2.0 * math.pi
        angleRight = math.pi / 2 + (i - 2) / 5.0 * 2.0 * math.pi
        xyLeft = (int(math.cos(angleLeft) * length + center_x), int(center_y - math.sin(angleLeft) * length))
        cv2.line(frame, xyFirst, xyLeft, (0, 0, 255), 2)
        xyRight = (int(math.cos(angleRight) * length + center_x), int(center_y - math.sin(angleRight) * length))
        cv2.line(frame, xyFirst, xyRight, (0, 0, 255), 2)

    # Отображаем кадр с красным крестом
    cv2.imshow('Camera with Red Pentagram', frame)

    # Нажмите 'q' для выхода
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Освобождаем ресурсы
cap.release()
cv2.destroyAllWindows()
