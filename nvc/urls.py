from django.urls import path
from django.contrib import admin
from nvc_app import views
urlpatterns = [
    path('admin/',admin.site.urls),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('email_password_reset/',views.EmailPasswordResetView.as_view(),name='email-password-reset'),
    path('reset_password/<uid>/<token>/',views.ResetPasswordView.as_view(),name='reset-password'),
    path('change_password/',views.UserChangePasswordView.as_view(),name='change_password'),
    path('create_ticket/',views.CreateTicket.as_view(),name='create_ticket'),
    #path('user_profile/',views.UserProfile.as_view(),name='user-profile')
   

]