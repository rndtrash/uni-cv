import cv2
import numpy as np
import sys

COLOR_RED = 0
COLOR_GREEN = 1
COLOR_BLUE = 2

red_bounds = (np.array([162, 52, 46]), np.array([179, 255, 255]))
green_bounds = (np.array([39, 20, 38]), np.array([88, 255, 255]))
blue_bounds = (np.array([102, 68, 89]), np.array([120, 255, 255]))


def get_color_mask(frame, color):
    if color == COLOR_RED:
        return cv2.inRange(frame, *red_bounds)
    elif color == COLOR_BLUE:
        return cv2.inRange(frame, *blue_bounds)
    elif color == COLOR_GREEN:
        return cv2.inRange(frame, *green_bounds)
    else:
        return np.zeros_like(frame[:, :, 0])


cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Не удалось открыть камеру")
    sys.exit(-1)

selected_color = COLOR_RED
kernel = np.ones((5, 5), np.uint8)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Ошибка при получении кадра")
        break

    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    color_mask = get_color_mask(hsv_frame, selected_color)

    opening = cv2.morphologyEx(color_mask, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(color_mask, cv2.MORPH_CLOSE, kernel)

    opened_output = cv2.bitwise_and(frame, frame, mask=opening)
    closed_output = cv2.bitwise_and(frame, frame, mask=closing)

    cv2.imshow('Original Image', frame)
    cv2.imshow('Opened Image (Noise Removed)', opened_output)
    cv2.imshow('Closed Image (Gaps Filled)', closed_output)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('r'):
        selected_color = COLOR_RED
    elif key == ord('g'):
        selected_color = COLOR_GREEN
    elif key == ord('b'):
        selected_color = COLOR_BLUE

# Освобождение ресурсов
cap.release()
cv2.destroyAllWindows()
