from django.urls import path
from . import views
from .views import UserUpdateAPIView,EmployerProfileEditView,UserDeleteAPIView
from django.urls import include, path
from rest_framework import routers



urlpatterns = [
    path("register", views.register, name="register"),
    path("login",views.login, name="login"),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('logout',views.logout,name='logout'),
    path('employer-profile/', views.EmployerProfile, name='employer_profile'),
    path('<str:username>/', UserUpdateAPIView.as_view()),
    path('employer-profile/<int:profile_id>/',EmployerProfileEditView.as_view()),
    path('delete/<str:username>/', UserDeleteAPIView.as_view(), name='user-delete'),
]



