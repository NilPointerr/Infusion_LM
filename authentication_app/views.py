from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import User
from leave_app.models import leaveForm_model, addholidays_model
from datetime import date, timedelta, datetime
# Create your views here.


def createUserView(request):

    get_department_value = User.department_choices
    get_role_value = User.role_choices
    get_employee_value = User.employee_choices

    context = {'get_department_value': get_department_value,
               'get_role_value': get_role_value,
               'get_employee_value': get_employee_value,
               }

    if request.method == "POST":
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirmpassword']
        image = request.FILES.get('profilepicture')

        birth_date = request.POST['birthdate']
        employee_joining_date = request.POST['employeejoiningdate']
        department = request.POST['department']
        role = request.POST['role']
        employee_type = request.POST['employeetype']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exist')
                return render(request, 'user_register.html')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'email already exist')
                return render(request, 'user_register.html')
            else:
                user = User.objects.create_user(first_name=first_name,
                                                last_name=last_name,
                                                username=username,
                                                email=email,
                                                password=password,
                                                image=image,
                                                birth_date=birth_date,
                                                employee_joining_date=employee_joining_date,
                                                department=department,
                                                role=role,
                                                employee_type=employee_type,


                                                )
                user.save()
                # return HttpResponse('user create')
                return redirect('login')
        else:
            messages.error(request, 'password does not match')
            return render(request, 'user_register.html')
    else:
        return render(request, 'user_register.html', context)


def loginUserView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            # if request.user.is_superuser ==
            login(request, user)
            return redirect('userdashboard', request.user.id)

            # else:
            # login(request,user)
            # return redirect('home')

        else:
            messages.error(request, 'Invalid Credentials')
            return render(request, 'user_login.html')
    else:
        return render(request, 'user_login.html')


def logoutUserView(request):
    logout(request)
    return redirect('login')


def userDashboardView(request, id):
    total_leaves = 18
    remain_leave_days = total_leaves
    holidays_datelist = addholidays_model.objects.values_list('date', flat=True)

    get_user_detail = User.objects.get(id=request.user.id)
    get_user_leave_forms = leaveForm_model.objects.filter(user=request.user)

    for getdata in get_user_leave_forms:
        start_date = getdata.start_date
        end_date = getdata.end_date

        leave_count = 0
        for i in range((end_date-start_date).days+1):
            print('i', i)
            days = start_date+timedelta(days=i)
            print('days: ', days)
            if days not in holidays_datelist and days.weekday() not in [5, 6]:
                leave_count += 1

                print('leave_count :', leave_count)
                remain_leave_days = total_leaves - leave_count
                if remain_leave_days <= 0:
                    print('remain_leave_days :', remain_leave_days)
                    remain_leave_days = 18

    context = {'get_user_detail': get_user_detail,
               'remain_leave_days': remain_leave_days}
    return render(request, 'user_dashboard.html', context)


def userProfileView(request, id):
    get_user_detail = User.objects.get(id=request.user.id)
    context = {'get_user_detail': get_user_detail}
    return render(request, 'user_profile.html', context)


def editUserProfileView(request, id):

    get_user_detail = User.objects.get(id=id)
    get_department_value = get_user_detail.department_choices
    get_role_value = get_user_detail.role_choices
    get_employee_value = get_user_detail.employee_choices

    if request.method == 'POST':
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirmpassword']
        image = request.FILES.get('profilepicture')

        birth_date = request.POST['birthdate']
        employee_joining_date = request.POST['employeejoiningdate']
        department = request.POST['department']
        role = request.POST['role']
        employee_type = request.POST['employeetype']

        get_user_detail.first_name = first_name
        get_user_detail.last_name = last_name
        get_user_detail.username = username
        get_user_detail.email = email
        if password == confirm_password:
            get_user_detail.set_password(password)
        # if image:
        get_user_detail.image = image
        get_user_detail.birth_date = birth_date

        get_user_detail.employee_joining_date = employee_joining_date
        get_user_detail.department = department
        get_user_detail.role = role
        get_user_detail.employee_type = employee_type
        get_user_detail.save()
        return redirect('userprofile')

    context = {
        'get_user_detail': get_user_detail,
        'get_department_value': get_department_value,
        'get_role_value': get_role_value,
        'get_employee_value': get_employee_value

    }
    return render(request, 'edit_userprofile.html', context)




# def changeUserPasswordView(request):
#     get_user_password=User.object.get(id=id)
#     if request.method == 'POST': 
#         get_user_password.old_password

#     return render(request,'change_userpassword.html')