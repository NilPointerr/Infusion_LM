from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from .views import (leave_form,manageleave,register_1,login_1,logout_1,home_1,accept_1,reject_1,
                    rejected_leaves,accepted_leaves,emp_detail,cancel_1,pending_leaves
                    ,canceled_leaves,undo_button,dashboard,user_profile,leave_request,holiday_list,
                    edit_profile,add_holidays,delete_holiday)

urlpatterns = [
    path('leaveform',leave_form,name='leaveform'),
    path('manage',manageleave,name='manage'),
    path('register',register_1,name='register'),
    path('',login_1,name='login'),
    path('logout',logout_1,name='logout'),
    path('home',home_1,name= 'home'),
    path('accept/<int:pk>/',accept_1,name='accept'),
    path('reject/<int:pk>/',reject_1,name='reject'),
    path('cancel/<int:pk>/',cancel_1,name='cancel'),
    path('empdetail/<int:pk>',emp_detail,name='empdetail'),
    path('rejectpage',rejected_leaves,name='rejectname'),
    path('acceptpage',accepted_leaves,name='acceptname'),
    path('pendingpage',pending_leaves,name='pendingpage'),
    path('cancelpage',canceled_leaves,name='cancelpage'),
    path('undo/<int:leave_form_id>/',undo_button,name='undo'),
    path('dashboard',dashboard,name="dashboard"),
    path('userprofile/<int:pk>',user_profile,name='userprofile'),
    path('editprofile/<int:pk>',edit_profile,name='editprofile'),
    path('leaverequest/<int:pk>',leave_request,name='leaverequest'),
    path('holidaylist',holiday_list,name='holidaylist'),               
    path('addholiday',add_holidays,name='addholiday'),
    path('deleteholiday/<int:pk>',delete_holiday,name='deleteholiday'),               
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)