import cv2
import numpy as np

COLOR_RED = 0
COLOR_GREEN = 1
COLOR_BLUE = 2

red_bounds = (np.array([162, 52, 46]), np.array([179, 255, 255]))
green_bounds = (np.array([39, 20, 38]), np.array([88, 255, 255]))
blue_bounds = (np.array([102, 68, 89]), np.array([120, 255, 255]))


# Функция для получения маски в зависимости от выбранного цвета
def get_color_mask(frame, color):
    if color == COLOR_RED:
        return cv2.inRange(frame, *red_bounds)
    elif color == COLOR_BLUE:
        return cv2.inRange(frame, *blue_bounds)
    elif color == COLOR_GREEN:
        return cv2.inRange(frame, *green_bounds)
    else:
        return np.zeros_like(frame[:, :, 0])


# Открытие камеры
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Не удалось открыть камеру")
    exit()

selected_color = COLOR_RED

# Структурный элемент для морфологических операций
kernel = np.ones((5, 5), np.uint8)

while True:
    ret, frame = cap.read()

    if not ret:
        print("Ошибка при получении кадра")
        break

    # Преобразование изображения в цветовое пространство HSV
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Получаем маску для выбранного цвета
    color_mask = get_color_mask(hsv_frame, selected_color)

    # Применение морфологических операций для удаления шумов
    color_mask = cv2.morphologyEx(color_mask, cv2.MORPH_OPEN, kernel)

    # Находим моменты изображения
    moments = cv2.moments(color_mask)

    # Площадь объекта (момент m00)
    area = moments['m00']

    # Если площадь объекта больше порогового значения (для исключения шумов)
    if area > 1000:
        # Вычисляем координаты центра масс объекта
        cx = int(moments['m10'] / moments['m00'])
        cy = int(moments['m01'] / moments['m00'])

        # Находим контуры объекта для построения ограничивающего прямоугольника
        contours, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            # Находим самый большой контур (считаем, что это объект)
            largest_contour = max(contours, key=cv2.contourArea)

            # Вычисляем ограничивающий прямоугольник
            x, y, w, h = cv2.boundingRect(largest_contour)

            # Рисуем черный прямоугольник вокруг объекта
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 0), 2)

            # Отображаем центр объекта
            cv2.circle(frame, (cx, cy), 5, (0, 0, 0), -1)  # Рисуем центр массы

    # Отображаем маску для проверки
    cv2.imshow('Color Mask', color_mask)

    # Отображение исходного изображения с прямоугольником и центром объекта
    cv2.imshow('Original Image with Bounding Box', frame)

    # Обработка нажатий клавиш
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('r'):
        selected_color = COLOR_RED # Выбор красного цвета
    elif key == ord('g'):
        selected_color = COLOR_GREEN # Выбор зеленого цвета
    elif key == ord('b'):
        selected_color = COLOR_BLUE # Выбор синего цвета

# Освобождение ресурсов
cap.release()
cv2.destroyAllWindows()
