from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
import json
from .models import *

# Create your views here.

# This is a context processor that shows on all templates
def categories(request):
    return {
        'categories': Category.objects.all()
    }


# This is a context processor that shows on all templates
def main(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user = user)
        order_items = OrderItem.objects.filter(order = order)
        cartItems = order.get_item_total       
    else:
        order_items = []
        order = {'get_item_total': 0}
        cartItems = 0
    context = {'cartItems': cartItems, 'order':order, 'order_items':order_items}
    return (context)


# This is for user registration
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Already Used')
                return redirect('register')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Already Used')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                return redirect('login')
        else:
            messages.info(request, 'Password Not The Same')
            return redirect('register')
    else:
        return render(request, 'store/register.html')


# This is for user login
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get ('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('login')
    else:
        return render(request, 'store/login.html')


# This is for user logout
def logout(request):
    auth.logout(request)
    return redirect('/')


# The main page that displays all available products
def home(request):
    products =  Product.objects.all()
    context = {'products': products}
    return render(request, 'store/home.html', context)



def orders(request):
    order = Order.objects.all()
    user = request.user
    orders = Order.objects.get(user = user)
    #orders = Order.objects.filter()
    context = {'orders':orders}
    return render( request, 'store/orders.html', context)



# This shows the ordered items based on the logged in user
# Unauthorized users cannot have cart
def cart(request):
    user = request.user
    order, created = Order.objects.get_or_create(user = user)
    order_items = OrderItem.objects.filter(order = order)
    cartItems = order.get_item_total
    context = {'cartItems': cartItems, 'order':order, 'order_items':order_items}
    return render(request, 'store/cart.html', context)



# The payment and order summary
def checkout(request):
    context = {'cartItems': cartItems, 'order':order, 'order_items':order_items}
    return render(request, 'store/checkout.html', context)



# Displays selected categories
def category_list(request, category_name):
    category = Category.objects.get(name=category_name)
    products = Product.objects.filter(category=category)
    context = {'products': products}
    return render(request, 'store/category.html', context)



# Functionality for updating a logged in users cart
def updateItem(request):
    data = json.loads(request.body)
    product_id = data['productId']    
    action = data['action']  

    customer = request.user
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(user = customer)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)


    if action == "add":
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == "remove":
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
                                                                        
    return JsonResponse('Item was added', safe=False)                               