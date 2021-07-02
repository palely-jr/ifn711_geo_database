from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="geo-home"),
    path('register', views.register, name="geo-register"),
    path('signin', views.signin, name="geo-signin"),
    path('signout', views.signout, name='geo-signout'),
    path('dashboard', views.dashboard, name="geo-dashboard"),
    path('upload/file', views.uploadItem, name='geo-uploadItem'),
    # path('upload/files', views.uploadItems, name='geo-uploadItem'),
    path('delete/files', views.deleteItem, name='geo-deleteFiles'),
    path('map/single/<int:item_id>/', views.mapsingle, name='geo-singlemap'),
    path('map/all', views.mapall, name='geo-mapall'),
    path('share/remove/<int:item_id>/<str:company_name>/', views.removeshare, name='geo-removeshare'),
    path('file/share/<int:item_id>/', views.sharefiles, name='geo-sharefile'),
    path('filestoragealoc', views.filestoragealoc, name='geo-filestoragealoc'),
    path('company', views.company, name='geo-company'),
    path('playground', views.playground, name='geo-playground'),
    path('companyregistration', views.companyregistration, name='geo-orgRegistration'),
    path('companydisp', views.companydisp, name='geo-companydisp')
]
