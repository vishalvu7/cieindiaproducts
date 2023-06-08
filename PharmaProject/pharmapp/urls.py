from . import views
from django.urls import path

urlpatterns = [
    path('',views.userHome, name='userhome'),
    path('home',views.home, name='home'),
    path('admin',views.adminLogin, name='admin'),
    path('edit',views.updateProduct, name='edit'),
    path('delete',views.deleteProduct, name='delete'),
    path('mail', views.sendEmail, name='mail'),
    path('menu',views.createProductCategory, name='menu'),
    path('userproducts',views.userproductonclick, name='userproductonclick'),
    path('viewadminproducts',views.viewAdminProduct, name='viewadminproducts'),
    path('about',views.aboutUs, name='about'),
    # path('bycategory',views.products_by_category, name='bycategory'),
    path('bycategory/<str:menu_name>/', views.products_by_category, name='bycategory'),
    path('logout',views.logOut, name='logout'),
    path('feedback',views.feedBack, name='feedback'),
    path('map',views.ourPresence, name='map'),
    path('delete_category/<int:category_id>/', views.delete_category, name='delete_category'),
    path('update_category/<int:category_id>/<int:children_id>/', views.update_category, name='update_category'),
    
    
    
]

