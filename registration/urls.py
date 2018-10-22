from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

app_name = "registration"

urlpatterns = [
    path('login', LoginView.as_view(template_name='registration/login.html'), name="login"),
    path('register', views.register, name="register"),
    path('logout', views.logout_view, name="logout"),
    path('ajax/auth', views.ajaxauth, name="ajaxauth"),

]