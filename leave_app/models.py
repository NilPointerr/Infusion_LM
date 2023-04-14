from django.db import models
# from authentication_app.models import User
from leave_management import settings
# Create your models here.
# from django.conf import settings

class leaveForm_model(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    typeofleave = [
        ('Sick Leave', 'Sick Leave'), 
        ('Casual Leave', 'Casual Leave'),
        ('Emergency Leave','Emergency Leave'),
        ('Maternity Leave','Maternity Leave'),
        ('Paternity Leave','Paternity Leave'),
        ('Bereavement Leave','Bereavement Leave'),
        ('Sabbatical Leave','Sabbatical Leave'),
        ('Compensatory Leave','Compensatory Leave'),
    ]
    leaveday = [
        ('Full day', 'Full Day'),
        ('Half Day', 'Half Day'),
    ]
    start_date = models.DateField()
    end_date = models.DateField()
    leave_days=models.IntegerField()
    leave_type = models.CharField(max_length=100, choices=typeofleave)
    reason=models.TextField()
    sub_leave = models.CharField(max_length=100, choices=leaveday)




class addholidays_model(models.Model):
    daylist=[
        ('Sunday','Sunday'),
        ('Monday','Monday'),
        ('Tuesday','Tuesday'),
        ('Wednesday','Wednesday'),
        ('Thursday','Thursday'),
        ('Friday','Friday'),
        ('Saturday','Saturday'),
    ]

    date=models.DateField()
    day=models.CharField(max_length=100,choices=daylist)
    festival_name=models.CharField(max_length=100)


    def __str__(self):
        return self.festival_name
