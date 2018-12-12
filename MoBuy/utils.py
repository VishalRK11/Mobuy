__author__ = 'Vishal'

import random
import string

from django.utils.text import slugify


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def order_id_generator(instance):
    order_id = random_string_generator()
    instance_class = instance.__class__
    print(instance.__class__)
    if instance_class.objects.filter(order_id=order_id).exists():
        return order_id_generator(instance=instance)
    return order_id


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.model)

    instance_class = instance.__class__
    qs_exists = instance_class.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = f"{slug}-{random_string_generator(size=4)}"
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug
