from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('orders/', views.orders, name='orders'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('register/', views.register, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logout, name='logout'),

    path('update_item/', views.updateItem, name='update_item'),

    path('search/<category_name>/', views.category_list, name='category_list')
]