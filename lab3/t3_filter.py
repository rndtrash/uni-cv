import cv2
import numpy as np
from t2_gauss_normalised import gaussian_kernel, normalize_kernel


def manual_convolution(image, kernel):
    image_height, image_width = image.shape
    kernel_size = kernel.shape[0]
    pad = kernel_size // 2

    # Добавляем отступы того же цвета, что и крайние пиксели, для того, чтобы обработать края изображения
    padded_image = np.pad(image, pad, mode='edge')
    output_image = np.zeros_like(image)

    for i in range(image_height):
        for j in range(image_width):
            # Извлекаем участок изображения, соответствующий размеру ядра
            region = padded_image[i:i + kernel_size, j:j + kernel_size]
            # Применяем свёртку: умножаем ядро на соответствующий участок изображения и суммируем
            output_image[i, j] = np.sum(region * kernel)

    return output_image


def apply_gaussian_filter_manual(image, kernel_size, sigma):
    kernel = gaussian_kernel(kernel_size, sigma)
    kernel = normalize_kernel(kernel)
    return manual_convolution(image, kernel)


if __name__ == "__main__":
    img = cv2.imread('images/1.png', cv2.IMREAD_GRAYSCALE)
    for m in [3, 5, 7]:
        for s in [1.0, 5.0]:
            filtered_img = apply_gaussian_filter_manual(img, m, s)
            cv2.imwrite(f'out_manual_m{m}_s{s}.png', filtered_img)
