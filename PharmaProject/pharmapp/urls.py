from . import views
from django.urls import path

urlpatterns = [
    path('',views.userHome, name='userhome'),
    path('home',views.home, name='home'),
    path('admin',views.adminLogin, name='admin'),
    path('edit',views.updateProduct, name='edit'),
    path('delete',views.deleteProduct, name='edit'),
    path('mail', views.sendEmail, name='mail'),
    path('menu',views.createProductCategory, name='menu'),
    path('userproducts',views.userproductonclick, name='userproductonclick'),
    path('viewadminproducts',views.viewAdminProduct, name='viewadminproducts'),
    
    
    
]