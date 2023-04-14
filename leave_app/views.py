from django.shortcuts import render,redirect
from .models import leaveForm_model,addholidays_model
from authentication_app.models import User
from django.core.mail import send_mail
from leave_management import settings
from datetime import date,datetime



# Create your views here.

def leaveFormView(request):
    
    leave_type_choice=leaveForm_model.typeofleave
    leave_day=leaveForm_model.leaveday
    context={'leave_type_choice':leave_type_choice,'leave_day':leave_day}

    if request.method=='POST':
        start_date=request.POST['startdate']
        end_date=request.POST['enddate']
        str_start_date = datetime.strptime(start_date, '%Y-%m-%d')
        str_end_date = datetime.strptime(end_date, '%Y-%m-%d')
        leave_days=(str_end_date - str_start_date).days + 1
        leave_type=request.POST['select_value']
        reason=request.POST['reason']
        sub_leave=request.POST['select_day']
        user = request.user # Get the logged-in user
        data=leaveForm_model.objects.create(start_date=start_date,end_date=end_date,leave_days=leave_days,leave_type=leave_type,reason=reason,sub_leave=sub_leave,user=user)
        data.save()
        # import pdb; pdb.set_trace()
        get_mailid=User.objects.get(id=user.id)
        subject='Applied For Leave'
        emailfrom=get_mailid.email
        recipientlist=[settings.EMAIL_HOST_USER]
        
        
        message=f"hello,I'm {get_mailid.first_name},applied for leave "
        
        send_mail(subject, message, emailfrom, recipientlist, fail_silently=False)
        return redirect('userdashboard',request.user.id)
    return render(request,'leave_form.html',context)



def holidaysListView(request):
    get_holidays_list=addholidays_model.objects.all()
    context={'get_holidays_list':get_holidays_list}
    return render(request,'holidays_list.html',context)