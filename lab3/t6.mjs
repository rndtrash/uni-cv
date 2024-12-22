import {Jimp} from 'jimp';

async function applyGaussianBlur(imagePath, outputImagePath, radius) {
    try {
        const image = await Jimp.read(imagePath);
        image.gaussian(radius);
        await image.write(outputImagePath);
        console.log(`Результат в файле ${outputImagePath}`);
    } catch (error) {
        console.error('Ошибка при применении фильтра Гаусса:', error);
    }
}

applyGaussianBlur('images/1.png', 'out_blurred_image_jimp.jpg', 5);
