import cv2
import sys
import numpy as np


def noop(x):
    pass


cv2.namedWindow('image')

cv2.createTrackbar('HMin', 'image', 0, 179, noop)
cv2.createTrackbar('SMin', 'image', 0, 255, noop)
cv2.createTrackbar('VMin', 'image', 0, 255, noop)
cv2.createTrackbar('HMax', 'image', 0, 179, noop)
cv2.createTrackbar('SMax', 'image', 0, 255, noop)
cv2.createTrackbar('VMax', 'image', 0, 255, noop)

cv2.setTrackbarPos('HMax', 'image', 179)
cv2.setTrackbarPos('SMax', 'image', 255)
cv2.setTrackbarPos('VMax', 'image', 255)

hMin = sMin = vMin = hMax = sMax = vMax = 0
phMin = psMin = pvMin = phMax = psMax = pvMax = 0

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Не удалось открыть камеру")
    sys.exit(-1)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Ошибка при получении кадра")
        break

    hMin = cv2.getTrackbarPos('HMin', 'image')
    sMin = cv2.getTrackbarPos('SMin', 'image')
    vMin = cv2.getTrackbarPos('VMin', 'image')

    hMax = cv2.getTrackbarPos('HMax', 'image')
    sMax = cv2.getTrackbarPos('SMax', 'image')
    vMax = cv2.getTrackbarPos('VMax', 'image')

    lower = np.array([hMin, sMin, vMin])
    upper = np.array([hMax, sMax, vMax])

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)
    output = cv2.bitwise_and(frame, frame, mask=mask)

    if (phMin != hMin) or (psMin != sMin) or (pvMin != vMin) or (phMax != hMax) or (psMax != sMax) or (pvMax != vMax):
        print("min = (%d , %d, %d), max = (%d, %d, %d)" % (hMin, sMin, vMin, hMax, sMax, vMax))
        phMin = hMin
        psMin = sMin
        pvMin = vMin
        phMax = hMax
        psMax = sMax
        pvMax = vMax

    cv2.imshow('image', output)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
