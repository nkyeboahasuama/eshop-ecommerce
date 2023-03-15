from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, blank=True, null=True)
    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_list', args=[self.name])


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()
    in_stock = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(upload_to='images/', default='images/lacoste.jfif')

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.ForeignKey(User,default=1, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=20, null=False)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([items.get_price_by_quantity for items in orderitems])
        return total

    @property
    def get_item_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([items.quantity for items in orderitems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.order)

    @property
    def get_price_by_quantity(self):
        total = self.product.price * self.quantity
        return total

