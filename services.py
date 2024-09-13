from django.core.exceptions import ValidationError
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


def get_path_upload_avatar(instance, file):
    return f"avatar/{instance.id}/{file}"


def get_path_upload_textfile(instance, file):
    return f"textfile/{instance.post_id}/{file}"


def get_path_upload_comments_images(instance, file):
    return f"comments_images/{instance.post_id}/{file}"
    

def validate_avatar(image):
    max_width = 600
    max_height = 600
    img = Image.open(image)


    if img.width > max_width or img.height > max_height:
        raise ValidationError(f"Изображение должно быть не более {max_width}x{max_height} пикселей.")

    if img.format.lower() not in ['jpg', 'jpeg', 'png']:
        raise ValidationError("Допустимые форматы изображений: JPG, JPEG, PNG")


def validate_size_upload_textfile(file):
    limit_upload_kb = 100

    if file.size > limit_upload_kb * 1024:
        raise ValidationError(f"Максимальный размер файла - {limit_upload_kb}килобайт")
    

def validate_upload_comments_images(image):
    fixed_width = 240

    img = Image.open(image)
    
    if img.format.lower() not in ['jpg', 'jpeg', 'png']:
        raise ValidationError("Допустимые форматы изображений: JPG, JPEG, PNG")


    width_percent = (fixed_width / float(img.size[0]))
    height_size = int((float(img.size[1]) * float(width_percent)))
    
    new_image = img.resize((fixed_width, height_size), Image.LANCZOS)

    output = BytesIO()
    new_image.save(output, format=img.format)
    output.seek(0)
    
    image_file = InMemoryUploadedFile(output, 'ImageField', image.name, 'image/jpeg', output.tell(), None)
    
    return image_file