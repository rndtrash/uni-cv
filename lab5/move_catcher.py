import cv2

i = 0


def main(kernel_size, standard_deviation, delta_tresh, min_area):
    global i
    i += 1

    video = cv2.VideoCapture('videos/src.mp4', cv2.CAP_ANY)

    ret, frame = video.read()

    # Перевод в серый цвет
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Сглаживание по Гауссу
    img = cv2.GaussianBlur(img, (kernel_size, kernel_size), standard_deviation)

    w = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # Создаем объект для записи
    video_writer = cv2.VideoWriter('videos/out_' + str(i) + '.mp4', fourcc, 25, (w, h))

    while True:
        print('Обрабатываю видео...')
        # Сохраняем предыдущий кадр
        old_img = img.copy()

        # Проверка кадра
        check, frame = video.read()
        if not check:
            break

        # Переводим кадр в серый и сглаживаем
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        img = cv2.GaussianBlur(img, (kernel_size, kernel_size), standard_deviation)

        # Модуль разницы двух кадров
        frame_diff = cv2.absdiff(img, old_img)

        # Фильтр если значение элемента меньше трешхолда то ставим 0, иначе 255
        # cv2.THRESH_BINARY - задает функцию по которой фильтруются элементы.
        # Возвращает значение трешхолда и отфильтрованный кадр
        thresh = cv2.threshold(frame_diff, delta_tresh, 255, cv2.THRESH_BINARY)[1]

        # Выделение контуров
        # cv2.RETR_EXTERNAL - выделяет невложенные контуры
        # cv2.CHAIN_APPROX_SIMPLE - сжимает горизонтальные вертикальные и диагональные сегменты и возвращает меньше точек контуров
        (contours, hierarchy) = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            # Площадь контура
            area = cv2.contourArea(contour)
            # Если больше или равно, то фиксируем движение
            if area >= min_area:
                video_writer.write(frame)
                break
    # Конец записи
    video_writer.release()
    print('Обработка завершена')


kernel_size = 3
standard_deviation = 50
delta_tresh = 60
min_area = 20
main(kernel_size, standard_deviation, delta_tresh, min_area)

kernel_size = 3
standard_deviation = 50
delta_tresh = 40
min_area = 5
main(kernel_size, standard_deviation, delta_tresh, min_area)

kernel_size = 5
standard_deviation = 50
delta_tresh = 70
min_area = 30
main(kernel_size, standard_deviation, delta_tresh, min_area)

kernel_size = 5
standard_deviation = 30
delta_tresh = 50
min_area = 15
main(kernel_size, standard_deviation, delta_tresh, min_area)

kernel_size = 11
standard_deviation = 70
delta_tresh = 60
min_area = 20
main(kernel_size, standard_deviation, delta_tresh, min_area)
