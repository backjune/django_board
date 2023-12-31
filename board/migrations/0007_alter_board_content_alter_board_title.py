# Generated by Django 4.2.4 on 2023-08-31 09:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('board', '0006_alter_customuser_options_board'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='content',
            field=models.TextField(max_length=1000, validators=[django.core.validators.MinLengthValidator(2)]),
        ),
        migrations.AlterField(
            model_name='board',
            name='title',
            field=models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(2)]),
        ),
    ]
