from datetime import datetime

from django.core.validators import MinValueValidator
from django.db.models import (CharField, IntegerField, ManyToManyField, Model,
                              SmallIntegerField)
from django.db.models.fields import PositiveSmallIntegerField
from rest_framework.fields import MaxValueValidator


class Author(Model):
    name = CharField(max_length=30)

    class Meta:
        verbose_name = 'Author'
        verbose_name_plural = 'Authors'


class Book(Model):
    name = CharField(max_length=60)
    edition = SmallIntegerField(
        validators=[
            MinValueValidator(1)
        ],
        default=1,
    )
    publication_year = SmallIntegerField(
        validators=[
            MaxValueValidator(datetime.now().year)
        ],
        help_text="Use the following format: <YYYY>"
    )
    authors = ManyToManyField(
        Author,
        'books',
    )

    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
