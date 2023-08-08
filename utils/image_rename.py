import os
import uuid


def crops_category_image(instance, filename):
    upload_to = 'corbel/crops-category/images'
    name, ext = filename.split('.')[0], filename.split('.')[1]
    filename = f'{name}-{uuid.uuid4()}.{ext}'
    return os.path.join(upload_to, filename)


def crops_image(instance, filename):
    upload_to = 'corbel/crops/images'
    name, ext = filename.split('.')[0], filename.split('.')[1]
    filename = f'{name}-{uuid.uuid4()}.{ext}'
    return os.path.join(upload_to, filename)


def crops_disease_image(instance, filename):
    upload_to = 'corbel/crops-disease/images'
    name, ext = filename.split('.')[0], filename.split('.')[1]
    filename = f'{name}-{uuid.uuid4()}.{ext}'
    return os.path.join(upload_to, filename)
