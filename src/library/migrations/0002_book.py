# Generated by Django 3.0.3 on 2020-02-24 16:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('edition', models.SmallIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)])),
                ('publication_year', models.SmallIntegerField(help_text='Use the following format: <YYYY>', validators=[django.core.validators.MaxValueValidator(2020)])),
                ('authors', models.ManyToManyField(related_name='books', to='library.Author')),
            ],
        ),
    ]
