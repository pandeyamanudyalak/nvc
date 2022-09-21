from django.urls import path
from django.contrib import admin
from nvc_app import views
urlpatterns = [
    path('admin/',admin.site.urls),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
   

]