from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    img = models.ImageField(upload_to='images/%y/%m/%d/', null=True, blank=True)
    category = models.CharField(
        max_length=50, 
        choices=[
            ('electronics', 'إلكترونيات'),
            ('fashion', 'أزياء'),
            ('home', 'المنزل'),
            ('books', 'كتب'),
            ('other', 'أخرى')
        ],
        default='other'
    )
    stock = models.PositiveIntegerField(default=1)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='products', null=True, blank=True)
    seller_phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=5.00)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    def total(self):
        return sum(item.product.price * item.quantity for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    
    def subtotal(self):
        return self.product.price * self.quantity

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField(CartItem)
    total = models.DecimalField(max_digits=10, decimal_places=2);status = models.CharField(max_length=20, default='pending')