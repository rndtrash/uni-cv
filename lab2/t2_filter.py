import cv2
import numpy as np
import sys

COLOR_RED = 0
COLOR_GREEN = 1
COLOR_BLUE = 2
COLOR_BLACK = 3
COLOR_WHITE = 4

# В OpenCV значение Hue находится в диапозоне [0; 180]
red_bounds = (np.array([162, 52, 46]), np.array([179, 255, 255]))
green_bounds = (np.array([39, 20, 38]), np.array([88, 255, 255]))
blue_bounds = (np.array([102, 68, 89]), np.array([120, 255, 255]))
black_bounds = (np.array([0, 0, 0]), np.array([180, 28, 84]))
white_bounds = (np.array([0, 0, 174]), np.array([180, 55, 255]))


def get_color_mask(frame, color):
    if color == COLOR_RED:
        return cv2.inRange(frame, *red_bounds)
    elif color == COLOR_BLUE:
        return cv2.inRange(frame, *blue_bounds)
    elif color == COLOR_GREEN:
        return cv2.inRange(frame, *green_bounds)
    elif color == COLOR_BLACK:
        return cv2.inRange(frame, *black_bounds)
    elif color == COLOR_WHITE:
        return cv2.inRange(frame, *white_bounds)
    else:
        return np.zeros_like(frame[:, :, 0])


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

    red_mask = get_color_mask(hsv_frame, COLOR_RED)
    green_mask = get_color_mask(hsv_frame, COLOR_GREEN)
    blue_mask = get_color_mask(hsv_frame, COLOR_BLUE)
    black_mask = get_color_mask(hsv_frame, COLOR_BLACK)
    white_mask = get_color_mask(hsv_frame, COLOR_WHITE)

    red_output = cv2.bitwise_and(frame, frame, mask=red_mask)
    green_output = cv2.bitwise_and(frame, frame, mask=green_mask)
    blue_output = cv2.bitwise_and(frame, frame, mask=blue_mask)
    black_output = cv2.bitwise_and(frame, frame, mask=black_mask)
    white_output = cv2.bitwise_and(frame, frame, mask=white_mask)

    cv2.imshow('Source', frame)
    cv2.imshow('Red Objects', red_output)
    cv2.imshow('Green Objects', green_output)
    cv2.imshow('Blue Objects', blue_output)
    cv2.imshow('Black Objects', black_output)
    cv2.imshow('White Objects', white_output)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
