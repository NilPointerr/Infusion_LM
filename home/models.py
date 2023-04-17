from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
# Create your models here.
from django.db import models




from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager
from leave_clone import settings




class User(AbstractUser):

    department_choices=(
                        ('FINANCE','FINANCE'),
                        ('SALES','SALES'),
                        ('SOFTWARE DEVELOPER','SOFTWARE DEVELOPER'),
                        ('HR','HR'),
    )

    role_choices=(
                    ('BDE','BDE'),
                    ('EMPLOYEE','EMPLOYEE'),
                    ('HR','HR'),
                )
    
    employee_choices=(
                        ('FULL-TIME','FULL-TIME'),
                        ('PART-TIME','PART-TIME'),
                        ('INTERN','INTERN'),

                     )

    first_name=models.CharField(max_length=30)
    last_name=models.CharField(max_length=30)
    username=models.CharField(max_length=30,unique=True)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=5000)
    image=models.ImageField(upload_to='images/',default=None)
    birth_date=models.DateField(null=True)
    employee_joining_date=models.DateField(null=True)
    department=models.CharField(max_length=100,choices=department_choices)
    role=models.CharField(max_length=100,choices=role_choices)
    employee_type=models.CharField(max_length=100,choices=employee_choices)

    object = UserManager()


    USERNAME_FIELD = 'username'
    # REQUIRED_FIELDS =[]

    def full_name(self):
        return self.first_name + "" + self.last_name






SICK = 'sick'
CASUAL = 'casual'
EMERGENCY = 'emergency'
STUDY = 'study'
MATERNITY = 'maternity'
BEREAVEMENT = 'bereavement'
QUARANTINE = 'quarantine'
COMPENSATORY = 'compensatory'
SABBATICAL = 'sabbatical'



class Leave_form(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,primary_key=True)
    typeofleave = [
        (SICK,'Sick Leave'),
        (CASUAL,'Casual Leave'),
        (EMERGENCY,'Emergency Leave'),
        (STUDY,'Study Leave'),
        (MATERNITY, 'Maternity Leave'),
        (BEREAVEMENT, 'Bereavement Leave'),
        (QUARANTINE, 'Self Quarantine'),
        (COMPENSATORY, 'Compensatory Leave'),
        (SABBATICAL, 'Sabbatical Leave')
    ]
    leaveday = [
        ('Full day', 'Full Day'),
        ('Half Day', 'Half Day'),
    ]
    statustype = [
        ('Pending','Pending'),
        ('Approved','Approved'),
        ('Cancel','Cancel'),
        ('Rejected','Rejected'),

    ]

    start_date = models.DateField()
    end_date = models.DateField()
    leave_type = models.CharField(max_length=100, choices=typeofleave)
    number_of_days = models.IntegerField(default=0)
    remaining_days = models.IntegerField(default=18)
    sub_leave = models.CharField(max_length=100, choices=leaveday)
    status = models.CharField(max_length=100,choices=statustype,default='Pending')
    reason = models.CharField(max_length=500,default='No reason')

    def __str__(self):
        return self.user.username
    

    def save(self, *args, **kwargs):
        # Calculate the number of days between the start and end dates
        delta = self.end_date - self.start_date
        self.number_of_days = delta.days + 1

        # Update the remaining days based on the number of days taken
        if str(self.remaining_days).isnumeric():
            self.remaining_days = int(self.remaining_days) - self.number_of_days

        # Call the superclass save method to save the object
        super(Leave_form, self).save(*args, **kwargs)
    # class Meta:

    #     managed = True
    #     db_table = 'leavein'
    

class Reason(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,primary_key=True)
    reason = models.CharField(max_length=500)

    def __str__(self):
        return self.user.username
    class Meta:
        db_table = 'reason'



class Holiday_list(models.Model):
    daylist=[
        ('Sunday','Sunday'),
        ('Monday','Monday'),
        ('Tuesday','Tuesday'),
        ('Wednesday','Wednesday'),
        ('Thursday','Thursday'),
        ('Friday','Friday'),
        ('Saturday','Saturday'),
    ]
    id = models.AutoField(primary_key=True)
    date=models.DateField()
    day=models.CharField(max_length=100,choices=daylist)
    festival_name=models.CharField(max_length=100)


    def __str__(self):
        return self.festival_name
    class Meta:
        ordering = ['date']