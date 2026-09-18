from django.db import models

# Create your models here.


# models.py
from django.db import models
from django.contrib.auth.models import User
from django.db.models import CharField, TextField
from django.db.models.base import Model
from django.db.models.deletion import CASCADE
from django.db.models.fields import DecimalField
from django.db.models.fields.related import ForeignKey


class Category(Model):
    title = CharField(max_length=100)
    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Categories"

class Product(Model):
    title = CharField(max_length=255)
    price = DecimalField(max_digits=12, decimal_places=2)
    category = ForeignKey('apps.Category', on_delete=CASCADE, related_name='products')

    def __str__(self):
        return self.title