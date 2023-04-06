from django.contrib import admin
from django.urls import path,include
from .views import (demo,manageleave,register_1,login_1,logout_1,home_1,accept_1,reject_1,
                    rejected_leaves,accepted_leaves,all_leaves,cancel_1,pending_leaves
                    ,canceled_leaves,undo_button,dashboard)

urlpatterns = [
    path('leaveform',demo,name='demo'),
    path('manage',manageleave,name='manage'),
    path('register',register_1,name='register'),
    path('',login_1,name='login'),
    path('logout',logout_1,name='logout'),
    path('home',home_1,name= 'home'),
    path('accept/<int:pk>/',accept_1,name='accept'),
    path('reject/<int:pk>/',reject_1,name='reject'),
    path('cancel/<int:pk>/',cancel_1,name='cancel'),
    path('empdetail/<int:pk>',all_leaves,name='empdetail'),
    path('rejectpage',rejected_leaves,name='rejectname'),
    path('acceptpage',accepted_leaves,name='acceptname'),
    path('pendingpage',pending_leaves,name='pendingpage'),
    path('cancelpage',canceled_leaves,name='cancelpage'),
    path('undo/<int:leave_form_id>/',undo_button,name='undo'),
    path('dashboard',dashboard,name="dashboard"),
    
]
