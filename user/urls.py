from django.urls import path

from user import views

urlpatterns = [
    path('otp/', views.OTPView.as_view(), name='otp_view'),

]