from django.urls import path, re_path, include

from . import views

urlpatterns = [
    path('', views.Index.as_view()),
    path('accounts/login', views.LoginForm.as_view()),
    path('accounts/register', views.RegistrationUser.as_view(), name='register'),
    path('room/<uuid>', views.CheckPassword.as_view()),
    path('room/<uuid>/change_file', views.ChangeFiles.as_view()),
    path('accounts/profile/', views.ProfileHandler.as_view()),
]
