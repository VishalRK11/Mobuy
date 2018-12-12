from django.db import models
from django.urls import reverse

from decimal import Decimal
from django.core.validators import MinValueValidator

from django.db.models import Q
from django.db.models.signals import pre_save

from MoBuy.utils import unique_slug_generator


class ProductManager(models.Manager):
    def featured(self):
        return self.get_queryset().filter(featured=True)

    def search(self, query):
        lookups = (Q(title__icontains=query) |
                   Q(description__icontains=query) |
                   Q(brand__icontains=query) |
                   Q(category__icontains=query)
                   )
        return self.get_queryset().filter(lookups).distinct()


CATEGORY_CHOICES = (
    ('apple', 'IOS'),
    ('android', 'Android'),
    ('windows', 'Windows'),
)


class Product(models.Model):
    title        = models.CharField(max_length=128)
    category     = models.CharField(max_length=16, null=True, blank=True, choices=CATEGORY_CHOICES)
    brand        = models.CharField(max_length=64, null=True, blank=True)
    model        = models.CharField(max_length=128, null=True, blank=True)
    slug         = models.SlugField(unique=True, blank=True, null=True)
    description  = models.TextField()
    price        = models.DecimalField(decimal_places=2, max_digits=20, validators=[MinValueValidator(Decimal('0.00'))])
    image        = models.ImageField(upload_to='products/', null=True, blank=True)
    featured     = models.BooleanField(default=False)
    units        = models.PositiveIntegerField(default=1, null=True, blank=True)
    added        = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    objects = ProductManager()

    def get_absolute_url(self):
        return reverse("products:detail", kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title


class Tag(models.Model):
    title       = models.CharField(max_length=120)
    slug        = models.SlugField()
    timestamp   = models.DateTimeField(auto_now_add=True)
    active      = models.BooleanField(default=True)
    products    = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return self.title


def set_tag_slug(sender, instance, *args, **kwargs):
    if sender and not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(set_tag_slug, sender=Tag)


def set_product_slug(sender, instance, *args, **kwargs):
    if sender and not instance.slug:
        instance.slug = unique_slug_generator(instance)


pre_save.connect(set_product_slug, sender=Product)