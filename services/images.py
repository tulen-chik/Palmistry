import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        raise Exception("Could not download the image.")

def edit_image(bg_image_path, avatar_image_url, place_name, output_image_path):
    # Загружаем фон
    bg_image = Image.open(bg_image_path)

    # Загружаем аватар по URL
    avatar = download_image(avatar_image_url)
    avatar = avatar.resize((800, 800))  # Изменяем размер аватара

    # Создаем маску для круга
    mask = Image.new('L', (avatar.width, avatar.height), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, avatar.width, avatar.height), fill=255)

    # Применяем маску к аватару
    avatar.putalpha(mask)

    # Определяем положение аватара (по центру)
    avatar_position = ((bg_image.width - avatar.width) // 2, (bg_image.height - avatar.height) // 2)

    # Добавляем аватар на фон
    bg_image.paste(avatar, avatar_position, avatar)

    # Устанавливаем шрифт и размер для текста
    font = ImageFont.truetype('public/Zametka_Parletter.otf', size=50)

    # Увеличиваем расстояние между аватаром и текстом
    text_offset = 70  # Увеличьте это значение, чтобы увеличить расстояние
    text_position = (bg_image.width // 2, avatar_position[1] + avatar.height + text_offset)

    # Добавляем текст
    draw = ImageDraw.Draw(bg_image)
    draw.text(text_position, place_name, fill="white", font=font, anchor="mm")

    # Сохраняем измененное изображение
    bg_image.save(output_image_path)


def edit_image_p(avatar_image_urls, place_names, output_image_path):
    # Загружаем фон
    bg_image = Image.open('public/bg_p.png')

    # Определяем размеры изображения и количество аватаров
    avatar_size = 800
    num_avatars = len(avatar_image_urls)
    spacing = 100  # Расстояние между аватарами
    total_width = (num_avatars * avatar_size) + ((num_avatars - 1) * spacing)

    # Вычисляем начальную позицию для центрирования аватаров
    start_x = (bg_image.width - total_width) // 2
    y_position = (bg_image.height - avatar_size) // 2  # Центруем по вертикали

    for i, (avatar_image_url, place_name) in enumerate(zip(avatar_image_urls, place_names)):
        # Загружаем аватар по URL
        avatar = download_image(avatar_image_url)
        avatar = avatar.resize((avatar_size, avatar_size))  # Изменяем размер аватара

        # Создаем маску для круга
        mask = Image.new('L', (avatar.width, avatar.height), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, avatar.width, avatar.height), fill=255)

        # Применяем маску к аватару
        avatar.putalpha(mask)

        # Определяем положение аватара
        avatar_position = (start_x + i * (avatar_size + spacing), y_position)

        # Добавляем аватар на фон
        bg_image.paste(avatar, avatar_position, avatar)

        # Устанавливаем шрифт и размер для текста
        font = ImageFont.truetype('public/Zametka_Parletter.otf', size=50)

        # Увеличиваем расстояние между аватаром и текстом
        text_offset = 30  # Расстояние между аватаром и текстом
        text_position = (avatar_position[0] + avatar_size // 2, avatar_position[1] + avatar_size + text_offset)

        # Добавляем текст
        draw = ImageDraw.Draw(bg_image)
        draw.text(text_position, place_name, fill="white", font=font, anchor="mm")

    # Сохраняем измененное изображение
    bg_image.save(output_image_path)