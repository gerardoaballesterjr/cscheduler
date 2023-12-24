import uuid, os

def uuid_generator():
    return uuid.uuid4().hex

def slug_generator(instance, slug=None):
    slug = slug if slug is not None else uuid_generator()
    if instance.__class__.objects.filter(slug=slug).exists():
        return slug_generator(instance, uuid_generator())
    return slug

def image_path(instance, filename):
    return f'{uuid_generator()}{os.path.splitext(filename)[-1]}'
