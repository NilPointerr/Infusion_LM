# Generated by Django 4.1.7 on 2023-04-14 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_alter_leave_form_number_of_days'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leave_form',
            name='remaining_days',
            field=models.IntegerField(default='', max_length=100),
        ),
    ]
