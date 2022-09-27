from django.urls import path,include
from django.contrib import admin
from nvc_app import views
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter






urlpatterns = [
    path('admin/',admin.site.urls),
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('email_password_reset/',views.EmailPasswordResetView.as_view(),name='email-password-reset'),
    path('reset_password/<uid>/<token>/',views.ResetPasswordView.as_view(),name='reset-password'),
    path('change_password/',views.UserChangePasswordView.as_view(),name='change_password'),
    path('create_ticket/',views.CreateTicket.as_view(),name='create_ticket'),
    path('all_ticket/',views.AllTickets.as_view(),name='all-ticket'),
    path('on_call_ticket/',views.OnCallView.as_view(),name='on-call-ticket'),
    path('closed_ticket/',views.ClosedTicketView.as_view(),name='closed_ticket'),
    path('visit_and_closed/',views.VisitAndClosedView.as_view(),name='visit-and-closed'),
    path('user_profile/<int:pk>/',views.UserProfile.as_view(),name='user-profile'),
  
    #path('file',views.PhotoViewSet.as_view(),name='file')
    #path('user_profile/',views.UserProfile.as_view(),name='user-profile')
   

] + static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)