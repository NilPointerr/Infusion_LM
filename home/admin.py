from django.contrib import admin
from .models import Leave_form,Reason,User,Holiday_list
# Register your models here.

admin.site.register(Leave_form)
admin.site.register(Reason)
admin.site.register(User)
admin.site.register(Holiday_list)
