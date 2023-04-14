from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from .models import Leave_form, Reason
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.conf import settings
from .models import User
from datetime import timedelta
from django.urls import reverse
from datetime import date, timedelta ,datetime
import calendar
from django.db.models import Sum



# Create your views here.


def register_1(request):

    get_department_value = User.department_choices
    get_role_value = User.role_choices
    get_employee_value = User.employee_choices

    context = {'get_department_value': get_department_value,
               'get_role_value': get_role_value,
               'get_employee_value': get_employee_value,
               }

    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        re_password = request.POST['re_password']
        image = request.FILES.get('profilepicture')
        birth_date = request.POST['birthdate']
        employee_joining_date = request.POST['employeejoiningdate']
        department = request.POST['department']
        role = request.POST['role']
        employee_type = request.POST['employeetype']

        if password == re_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exist')
                return render(request, 'register.html')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'email already exist')
                return render(request, 'register.html')
            else:
                user = User.objects.create_user(
                    first_name=first_name,
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

                return redirect('/dashboard')
        else:
            messages.error(request, 'password does not match')
            return render(request, 'register.html')
    else:
        return render(request, 'register.html', context)


def login_1(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_superuser:
                login(request, user)
                print(user.get_username)
                return redirect('/dashboard')

            else:
                login(request, user)
                return redirect('/dashboard')

        else:
            messages.error(request, 'Invalid credentials')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


def logout_1(request):
    logout(request)
    return redirect('login')


def home_1(request):
    return render(request, 'logout.html')


@login_required
def leave_form(request):
    leavetype = Leave_form.typeofleave
    subleave = Leave_form.leaveday
    context = {
        "leave_type_choice": leavetype,
        "leave_day": subleave,
    }
    leave = None

    if request.method == "POST":
        startdate = request.POST['startdate']
        enddate = request.POST['enddate']
        leavetype = request.POST['select_value']
        subleave = request.POST['select_day']
        reason = request.POST['reason']
        user = request.user

        remaining_days = 0
        working_days = 0
        if startdate and enddate:  # check if startdate and enddate are not empty
            if Leave_form.objects.filter(user=user).exists():
                user_profile = Leave_form.objects.get(user=user)
                remaining_days = int(user_profile.remaining_days)
                holidays_datelist = [date(2023, 1, 14), date(2023, 1, 26), date(2023, 3, 18), date(2023, 8, 11),
                                    date(2023, 8, 15), date(2023, 8, 19), date(2023, 10, 5), date(2023, 10, 24),
                                    date(2023, 10, 25), date(2023, 10, 26)]
                num_days = (datetime.strptime(enddate, '%Y-%m-%d') - datetime.strptime(startdate, '%Y-%m-%d')).days + 1
                working_days = 0
                for j in range(num_days):
                    day = datetime.strptime(startdate, '%Y-%m-%d') + timedelta(days=j)
                    if day.weekday() not in [5, 6] and day.date() not in holidays_datelist:
                        working_days += 1

                remaining_days -= working_days
                user_profile.remaining_days = remaining_days
                user_profile.save()

            else:
                user_profile = None

            # Create the Leave_form object only if startdate and enddate are not empty
            leave = Leave_form(start_date=startdate, end_date=enddate,
                            leave_type=leavetype, sub_leave=subleave,
                            reason=reason, user=user)
            leave.number_of_days = working_days
            leave.remaining_days = remaining_days
            if leave.remaining_days <= 0:
                leave.remaining_days = 0
            leave.save()

            return redirect(reverse('leaverequest', args=[leave.user_id]))

    return render(request, 'leave.html', context)


def manageleave(request):
    leave_forms = Leave_form.objects.all()
    users = User.objects.all()
    context = {
        'leave_forms': leave_forms,
        'users': users
    }
    return render(request, 'manage_leave.html', context)


def accept_1(request, pk):
    user = User.objects.get(pk=pk)
    obj = get_object_or_404(Leave_form, user_id=pk)
    obj.status = 'Approved'
    obj.save()

    if 'description' in request.POST:
        reason_text = request.POST.get('description')
    else:
        reason_text = 'No reason provided.'

    try:
        reason_obj = Reason.objects.filter(user_id=pk).latest('pk')
    except Reason.DoesNotExist:
        reason_obj = Reason(user_id=pk, reason='No reason provided.')
        reason_obj.save()

    reason_obj.reason = reason_text
    reason_obj.save()

    message = f"""Dear {user.username},<br><br>
                We happy to inform you that your leave application for the following period has been approved:<br><br>
                <head>
                   
                    <style>
                        table {{
                            border-collapse: collapse;
                        }}
                        th, td {{
                            border: 1px solid black;
                            padding: 5px;
                        }}
                        th {{
                            background-color: #ccc;
                        }}
                    </style>

                </head>

                <table style="border: 1px solid black;">
                    <tr>
                    <th>Start date</th>
                    <td>{obj.start_date}</td>
                    </tr>
                    <th>End date</th>
                    <td>{obj.end_date}</td>
                    </tr>
                    <tr>
                    <th>Leave Type</th>
                    <td>{obj.leave_type}</td>
                    </tr>
                    <tr>
                    <th>Sub leave</th>
                    <td>{obj.sub_leave}</td>
                    </tr>
                    <tr>
                    <th>Satus</th>
                    <td>{obj.status}</td>
                    </tr>
                    <tr>
                    <th>Reason </th>
                    <td>{reason_text}</td>
                    </tr>
                </table><br>
                If you have any questions, please don't hesitate to reach out to us.<br><br>
                Regards,<br>
                The HR Team"""

    send_mail(
        'Leave Status',
        message,
        'nilesh.ultragmaes@gmail.com',
        [user.email],
        fail_silently=False,
    )

    return redirect('/dashboard')


def reject_1(request, pk):
    user = User.objects.get(pk=pk)
    obj = get_object_or_404(Leave_form, user_id=pk)
    obj.status = 'Rejected'
    obj.save()

    if 'description' in request.POST:
        reason_text = request.POST.get('description')
    else:
        reason_text = 'No reason provided.'

    try:
        reason_obj = Reason.objects.filter(user_id=pk).latest('pk')
    except Reason.DoesNotExist:
        # Handle the case where there are no Reason objects for the given user_id
        # For example, you could create a new Reason object:
        reason_obj = Reason(user_id=pk, reason='No reason provided.')
        reason_obj.save()

    reason_obj.reason = reason_text
    reason_obj.save()

    message = f"""Dear {user.username},<br><br>
                We regret to inform you that your leave application for the following period has been declined:<br><br>
                <head>
                
                    <style>
                        table {{
                            border-collapse: collapse;
                        }}
                        th, td {{
                            border: 1px solid black;
                            padding: 5px;
                        }}
                        th {{
                            background-color: #ccc;
                        }}
                    </style>

                </head>

                <table style="border: 1px solid black;">
                    <tr>
                    <th>Start date</th>
                    <td>{obj.start_date}</td>
                    </tr>
                    <th>End date</th>
                    <td>{obj.end_date}</td>
                    </tr>
                    <tr>
                    <th>Leave Type</th>
                    <td>{obj.leave_type}</td>
                    </tr>
                    <tr>
                    <th>Sub leave</th>
                    <td>{obj.sub_leave}</td>
                    </tr>
                    <tr>
                    <th>Status</th>
                    <td>{obj.status}</td>
                    </tr>
                    <tr>
                    <th>Reason</th>
                    <td>{reason_text}</td>
                    </tr>
                </table><br>
                If you have any questions, please don't hesitate to reach out to us.<br><br>
                Regards,<br>
                The HR Team"""

    send_mail(
        'Leave Status',
        '',
        'nilesh.ultragmaes@gmail.com',
        [user.email],
        fail_silently=False,
        html_message=message,
    )
    return redirect('/dashboard')


def cancel_1(request, pk):
    user = User.objects.get(pk=pk)
    obj = get_object_or_404(Leave_form, user_id=pk)
    obj.status = 'Canceled'
    obj.save()
    # message = f"Dear {user.username},\n\nWe regret to inform you that your leaves are canceled.\n\nRegards,\nThe HR Team"

    # send_mail(
    #     'Leave Status',
    #      message,
    #     'nilesh.ultragmaes@gmail.com',
    #     [user.email],
    #     fail_silently=False,
    # )
    return redirect('/dashboard')


def emp_detail(request, pk):
    emp = Leave_form.objects.get(user_id=pk)
    emp_user = User.objects.get(pk=pk)
    con = {'emp': emp,
           'emp_user': emp_user}
    return render(request, "emp_detail.html", con)


def pending_leaves(request):
    pending = Leave_form.objects.filter(status="Pending")
    con = {'pending': pending}
    return render(request, "pending_leaves.html", con)


def accepted_leaves(request):
    accept = Leave_form.objects.filter(status="Approved")
    con = {'accept': accept}
    return render(request, "accepted_leave.html", con)


def rejected_leaves(request):
    reject = Leave_form.objects.filter(status="Rejected")
    con = {'reject': reject}
    return render(request, "rejected_leave.html", con)


def canceled_leaves(request):
    cancel = Leave_form.objects.filter(status="Canceled")
    total_canceled_leaves = cancel.count()
    print(total_canceled_leaves)
    con = {'cancel': cancel, 'total_canceled_leaves': total_canceled_leaves}
    return render(request, "canceled_leave.html", con)


def undo_button(request, leave_form_id):
    leave_form = Leave_form.objects.get(user_id=leave_form_id)
    if leave_form.status == 'Approved':
        leave_form.status = 'Pending'
        leave_form.save()
        return redirect("/acceptpage")
    elif leave_form.status == "Rejected":
        leave_form.status = 'Pending'
        leave_form.save()
        return redirect("/rejectpage")
    else:
        leave_form.status = 'Pending'
        leave_form.save()
        return redirect("/cancelpage")


def dashboard(request):
    accept = Leave_form.objects.filter(status="Approved")
    total_accept_leaves = accept.count()

    reject = Leave_form.objects.filter(status="Rejected")
    total_reject_leaves = reject.count()

    pending = Leave_form.objects.filter(status="Pending")
    total_pending_leaves = pending.count()

    cancel = Leave_form.objects.filter(status="Canceled")
    total_canceled_leaves = cancel.count()

    all = Leave_form.objects.all()
    total_leaves = all.count()

    superuser_count = User.objects.filter(is_superuser=True).count()
    total_user = User.objects.all().count()
    Employee = total_user-superuser_count

    # count dayss between startday and endday excluding saturday and sunday



    user = request.user
    leaves = Leave_form.objects.filter(user=user)
    # holidays_datelist = [date(2023, 1, 14), date(2023, 1, 26), date(2023, 3, 18), date(2023, 8, 11),
    #                     date(2023, 8, 15), date(2023, 8, 19), date(2023, 10, 5), date(2023, 10, 24),
    #                     date(2023, 10, 25), date(2023, 10, 26)]

    # for i in leaves:
    #     start_date = i.start_date
    #     end_date = i.end_date
    #     num_days = (end_date - start_date).days + 1
    #     working_days = 0

    #     # # Add previous number of days to working days
    #     # previous_days = int(i.number_of_days)
    #     # working_days += previous_days

    #     for j in range(num_days):
    #         day = start_date + timedelta(days=j)
    #         if day.weekday() not in [5, 6] and day not in holidays_datelist:
    #             working_days += 1

    #     # Count the last Saturday of the month
    #     last_day = calendar.monthrange(end_date.year, end_date.month)[1]
    #     last_saturday = date(end_date.year, end_date.month, last_day)
    #     while last_saturday.weekday() != calendar.SATURDAY:
    #         last_saturday -= timedelta(days=1)

    #     # Check if the last Saturday falls within the leave period
    #     if last_saturday >= start_date and last_saturday <= end_date:
    #         working_days += 1

    #     remaining_days = 18 - working_days
    #     i.remaining_days = remaining_days
    #     i.number_of_days = working_days

    #     if i.remaining_days <= 0:
    #         i.remaining_days = 0
    #     i.save()


    con = {'total_canceled_leaves': total_canceled_leaves,
           'total_accept_leaves': total_accept_leaves,
           'total_reject_leaves': total_reject_leaves,
           'total_pending_leaves': total_pending_leaves,
           'total_leaves': total_leaves,
           'Employee': Employee,
           'remaining_leaves': leaves}
    return render(request, 'base.html', con)


def user_profile(request, pk):
    emp_user = User.objects.get(pk=pk)
    con = {
        'emp_user': emp_user}
    return render(request, 'user_profile.html', con)


def leave_request(request,pk):
    user = User.objects.get(pk=pk)
    obj = get_object_or_404(Leave_form, user_id=pk)

    # message = f"""Dear {user.username},<br><br>
    #                 We are happy to inform you that your leave application for the following period has been sent Successfully:<br><br>
    #                 <head>
    #                     <style>
    #                         table {{
    #                             border-collapse: collapse;
    #                         }}
    #                         th, td {{
    #                             border: 1px solid black;
    #                             padding: 5px;
    #                         }}
    #                         th {{
    #                             background-color: #ccc;
    #                         }}
    #                     </style>
    #                 </head>

    #             <table style="border: 1px solid black;">
    #                 <tr>
    #                 <th>Start date</th>
    #                 <td>{obj.start_date}</td>
    #                 </tr>
    #                 <th>End date</th>
    #                 <td>{obj.end_date}</td>
    #                 </tr>
    #                 <tr>
    #                 <th>Leave Type</th>
    #                 <td>{obj.leave_type}</td>
    #                 </tr>
    #                 <tr>
    #                 <th>Sub leave</th>
    #                 <td>{obj.sub_leave}</td>
    #                 </tr>
    #                 <tr>
    #                 <th>Status</th>
    #                 <td>{obj.status}</td>
    #                 </tr>
    #                 <tr>
    #             </table><br>
    #             If you have any questions, please don't hesitate to reach out to us.<br><br>
    #             Regards,<br>
    #             The HR Team"""
    # send_mail(
    #     'Leave Status',
    #     message,
    #     '',
    #     ['purohit3133@gmail.com'],
    #     fail_silently=False,
    # )

    return redirect('/dashboard')


def holiday_list(request):
    return render(request,'holiday_list.html')


def edit_profile(request,pk):
    edit_user = User.objects.get(pk=pk)
    get_department_value = User.department_choices
    get_role_value = User.role_choices
    get_employee_value = User.employee_choices

    context = {
        'get_department_value': get_department_value,
        'get_role_value': get_role_value,
        'get_employee_value': get_employee_value,
        'edit_user': edit_user,
               }

    #logged in user can edit his profile
    if request.method == 'POST':
        edit_user.first_name = request.POST['first_name']
        edit_user.last_name = request.POST['last_name']
        edit_user.username = request.POST['username']
        if 'profilepicture' in request.FILES:
            edit_user.image = request.FILES['profilepicture']
        else:
            # set the previous image if there is no new picture uploaded
            edit_user.image = edit_user.image
        edit_user.birth_date = request.POST['birthdate']
        edit_user.department = request.POST['department']
        edit_user.role = request.POST['role']
        edit_user.employee_type = request.POST['employeetype']
        edit_user.save() 
        print("data saved")
        return redirect(reverse('userprofile', args=[edit_user.pk]))

                
    return render(request, 'edit_profile.html', context)

    