# Generated by Django 3.2.12 on 2023-04-04 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='birth_date',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='employee_joining_date',
            field=models.DateField(null=True),
        ),
    ]
