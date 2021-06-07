from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="geo-home"),
    path('register', views.register, name="geo-register"),
    path('signin', views.signin, name="geo-signin"),
    path('signout', views.signout, name='geo-signout'),
    path('dashboard', views.dashboard, name="geo-dashboard"),
    path('upload/file', views.uploadItem, name='geo-uploadItem'),
    path('delete/files', views.deleteItem, name='geo-deleteFiles'),
    path('filestoragealoc', views.filestoragealoc, name='geo-filestoragealoc'),
    path('company', views.company, name='geo-company'),
    path('playground', views.playground, name='geo-playground'),
    path('companyregistration', views.companyregistration, name='geo-orgRegistration')
]
