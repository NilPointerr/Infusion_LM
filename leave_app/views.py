from django.shortcuts import render,redirect
from .models import leaveForm_model
from  authentication_app.views import User
from django.core.mail import send_mail
from leave_management import settings
from django.http import HttpResponse



# Create your views here.

def leaveFormView(request):
    
    leave_type_choice=leaveForm_model.typeofleave
    leave_day=leaveForm_model.leaveday
    context={'leave_type_choice':leave_type_choice,'leave_day':leave_day}

    if request.method=='POST':
        start_date=request.POST['startdate']
        end_date=request.POST['enddate']
        leave_type=request.POST['select_value']
        sub_leave=request.POST['select_day']
        user = request.user # Get the logged-in user
        data=leaveForm_model.objects.create(start_date=start_date,end_date=end_date,leave_type=leave_type,sub_leave=sub_leave,user=user)
        data.save()
        # import pdb; pdb.set_trace()
        get_mailid=User.objects.get(id=user.id)
        subject='Applied For Leave'
        emailfrom=get_mailid.email
        recipientlist=[settings.EMAIL_HOST_USER]
        
        
        message=f"hello,I'm {get_mailid.first_name},applied for leave "
        
        send_mail(subject, message, emailfrom, recipientlist, fail_silently=False)
    return render(request,'leave_form.html',context)
