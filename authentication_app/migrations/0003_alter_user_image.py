# Generated by Django 3.2.12 on 2023-04-04 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication_app', '0002_auto_20230404_0735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='image',
            field=models.ImageField(default=None, upload_to='static/images'),
        ),
    ]
