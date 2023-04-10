from . import views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('registerform/',views.createUserView,name='register'),
    path('',views.loginUserView,name='login'),
    path('userdetails/<int:id>',views.displayUserDetails,name='userdetails'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)