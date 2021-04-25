from django.urls import path
from . import views
urlpatterns = [
    path('', views.home, name="geo-home"),
    path('register', views.register, name="geo-register"),
    path('signin', views.signin, name="geo-signin"),
]