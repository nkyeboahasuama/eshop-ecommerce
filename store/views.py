from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import json
from .models import *

# Create your views here.

def categories(request):
    return {
        'categories': Category.objects.all()
    }


def main(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer)
        order_items = OrderItem.objects.filter(order = order)
        cartItems = order.get_item_total       
    else:
        order_items = []
        order = {'get_item_total': 0}

    context = {'cartItems': cartItems, 'order':order, 'order_items':order_items}
    return (context)


def home(request):
    products =  Product.objects.all()
    context = {'products' : products}
    return render(request, 'store/home.html', context)


def cart(request):
    return render(request, 'store/cart.html')


def checkout(request):
    return render(request, 'store/checkout.html')


def category_list(request, category_name):
    category = Category.objects.get(name=category_name)
    products = Product.objects.filter(category=category)

    context = {'products': products}
    return render(request, 'store/category.html', context)

def updateItem(request):
    data = json.loads(request.body)
    product_id = data['productId']    
    action = data['action']  

    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer = customer)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)


    if action == "add":
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == "remove":
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
                                                                        
    return JsonResponse('Item was added', safe=False)                               