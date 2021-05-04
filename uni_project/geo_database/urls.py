from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="geo-home"),
    path('register', views.register, name="geo-register"),
    path('signin', views.signin, name="geo-signin"),
    path('signout', views.signout, name='geo-signout'),
    path('upload/file', views.uploadItem, name='geo-uploadItem'),
    path('delete/files', views.deleteItem, name='geo-deleteFiles')
]
