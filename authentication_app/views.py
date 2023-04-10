from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login
from .models import User


# Create your views here.

def createUserView(request):
    
    get_department_value=User.department_choices
    get_role_value=User.role_choices
    get_employee_value=User.employee_choices

    context={ 'get_department_value':get_department_value,
              'get_role_value':get_role_value, 
              'get_employee_value':get_employee_value,
            }

    if request.method == "POST":
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirmpassword']
        image = request.FILES.get('profilepicture')
        print(image)
        birth_date=request.POST['birthdate']
        employee_joining_date=request.POST['employeejoiningdate']
        department=request.POST['department']
        role=request.POST['role']
        employee_type=request.POST['employeetype']

        if password == confirm_password:
            if User.objects.filter(username = username).exists():
                messages.error(request,'Username already exist')
                return render(request,'user_register.html')
            elif User.objects.filter(email = email).exists():
                messages.error(request,'email already exist')
                return render(request,'user_register.html')
            else:
                user=User.objects.create_user(  first_name = first_name,
                                                last_name = last_name,
                                                username = username,
                                                email=email,
                                                password = password,
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
            messages.error(request,'password does not match')
            return render(request,'user_register.html')
    else: 
        return render(request,'user_register.html',context)
    


def loginUserView(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username = username,password = password)
        if user is not None:
            # if request.user.is_superuser ==
                login(request,user)
                return redirect('userdetails',request.user.id)
                
            # else:
                # login(request,user)
                # return redirect('home')

        else:
            messages.error(request,'Invalid Credentials')
            return render(request,'user_login.html')
    else:
        return render(request,'user_login.html')
    

def displayUserDetails(request,id):
    get_user_detail=User.objects.get(id=request.user.id)
    context={'get_user_detail':get_user_detail}
    return render(request,'user_dashboard.html',context)














































































# def demoView(request):
   
#     return render(request,'demo.html')



# def createUserView(request):
#     user_type_choices=createUserModel.objects.all() 
#     userchoices = createUserModel.userchoices    
                 
#     context={
#             "user_type_choices" : user_type_choices,
#             'user_type_choices':userchoices
#             }
    
#     if request.method == 'POST':
        
#         name = request.POST["name"]
#         email =  request.POST["email"]
#         number=  request.POST["number"]
#         password=  request.POST["password"]
#         select_value=request.POST['select_value']


#         register=createUserModel(name=name,email=email,number=number,password=password,user_type=select_value)
#         register.save()
#         return redirect('login')
    
#     return render(request,'user_register.html',context)


# def loginUserView(request):
#     if request.method == 'POST':
#         email_id=request.POST['email_id']
#         password=request.POST['password']
        
#         user=authenticate(username="ashok",password=password)
#         if user is not None:
#             login(request,user)
#             return render(request,'demo.html')
#         else:
#             return HttpResponse('login failed')
    
#     return render(request,'user_login.html')
    

    
    
