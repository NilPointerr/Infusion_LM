from . import views
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [
    path('registerform/',views.createUserView,name='register'),
    path('',views.loginUserView,name='login'),
    path('logout/',views.logoutUserView,name='logout'),
    path('userdashboard/<int:id>',views.userDashboardView,name='userdashboard'),
    path('userprofile/<int:id>',views.userProfileView,name='userprofile')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)