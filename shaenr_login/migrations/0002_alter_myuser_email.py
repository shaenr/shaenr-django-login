# Generated by Django 4.0.4 on 2022-04-19 03:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shaenr_login', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='email',
            field=models.EmailField(max_length=255, unique=True),
        ),
    ]
