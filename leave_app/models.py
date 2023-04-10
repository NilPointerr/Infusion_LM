from django.db import models
# from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

from leave_management import settings
# Create your models here.


class leaveForm_model(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    typeofleave = [
        ('Paid Leave', 'Paid Leave'), 
        ('Unpaid Leave', 'Unpaid Leave'),
    ]
    leaveday = [
        ('Full day', 'Full Day'),
        ('Half Day', 'Half Day'),
    ]
    start_date = models.DateField()
    end_date = models.DateField()
    leave_type = models.CharField(max_length=100, choices=typeofleave)
    sub_leave = models.CharField(max_length=100, choices=leaveday)
