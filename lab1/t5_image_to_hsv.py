import cv2

image = cv2.imread('images/img1.bmp')

if image is None:
    print("Ошибка открытия изображения")
    exit()

# меняем цвета в палитру hsv
hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Исходное
resizeOriginalImage = cv2.resize(image, (640,480))
cv2.imshow('Source Image', resizeOriginalImage)

# HSV
resizeHSVImage = cv2.resize(hsv_image, (640,480))
cv2.imshow('Converted to HSV', resizeHSVImage)

cv2.waitKey(0)

cv2.destroyAllWindows()
