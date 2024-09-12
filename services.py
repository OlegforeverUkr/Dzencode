from django.core.exceptions import ValidationError
from PIL import Image


def get_path_upload_avatar(instance, file):
    return f"avatar/{instance.id}/{file}"


def validate_size_upload_textfile(file):
    limit_upload_kb = 100

    if file.size > limit_upload_kb * 1024:
        raise ValidationError(f"Максимальный размер файла - {limit_upload_kb}килобайт")
    

def validate_avatar(image):
    max_width = 320
    max_height = 240
    img = Image.open(image)


    if img.width > max_width or img.height > max_height:
        raise ValidationError(f"Изображение должно быть не более {max_width}x{max_height} пикселей.")

    if img.format.lower() not in ['jpg', 'jpeg', 'png', 'gif']:
        raise ValidationError("Допустимые форматы изображений: JPG, JPEG, PNG, GIF.")
