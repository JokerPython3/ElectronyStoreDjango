from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import LoginForms, RegisterForms
from .models import Product, Cart, CartItem, Order
from django.db import transaction
from django.db.models import Q

def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = RegisterForms(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            messages.success(request, "Account created success")
            return redirect("login")
    else:
        form = RegisterForms()
    return render(request, "accounts/register.html", context={"form": form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        form = LoginForms(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForms()
    return render(request, "accounts/login.html", context={"form": form})

@login_required
def home(request):
    q = request.GET.get('q', '')
    cat = request.GET.get('category', '')
    sort = request.GET.get('sort', '-created_at')
    
    products = Product.objects.all()
    
    if cat:
        products = products.filter(category=cat)
    if q:
        products = products.filter(
            Q(name__icontains=q) |
            Q(description__icontains=q) |
            Q(category__icontains=q)
        ).distinct()
    
    if sort == 'price':
        products = products.order_by('price')
    elif sort == '-price':
        products = products.order_by('-price')
    elif sort == 'name':
        products = products.order_by('name')
    else:
        products = products.order_by('-created_at')

    cart, _ = Cart.objects.get_or_create(user=request.user)
    
    return render(request, "accounts/home.html", {
        "products": products,
        "cart": cart,
        "q": q,
        "current_category": cat,
        "current_sort": sort,
        "categories": Product._meta.get_field('category').choices,
    })

@login_required
def add_product(request):
    if request.method == "POST":
        try:
            product = Product.objects.create(
                name=request.POST.get("name"),
                description=request.POST.get("description"),
                price=request.POST.get("price"),
                category=request.POST.get("category"),
                img=request.FILES.get("image"),
                seller=request.user,
                stock=1
            )
            messages.success(request, "done add")
            return redirect("home")
        except Exception as e:
            messages.error(request, "error adding aitem")
    return redirect("home")

@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    return render(request, "accounts/cart.html", {"cart": cart})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
        item.save()
    messages.success(request, "done add to cart")
    return redirect("home")

@login_required
def buy(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, _ = Cart.objects.get_or_create(user=request.user)
    item, _ = CartItem.objects.get_or_create(cart=cart, product=product)
    item.quantity += 1
    item.save()
    order = Order.objects.create(user=request.user, total=product.price)
    order.items.add(item)
    order.save()
    messages.success(request, "done")
    return redirect("purchases")

@login_required
def purchases(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "accounts/purchases.html", {"orders": orders})

@login_required
def orders_view(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "accounts/orders.html", {"orders": orders})

@login_required
def profile(request):
    return render(request, "accounts/profile.html", {"user": request.user})

@login_required
@transaction.atomic
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    if not cart.items.exists():
        messages.error(request, "السلة فارغة")
        return redirect("cart")
    try:
        total = cart.total()
        order = Order.objects.create(user=request.user, total=total)
        for item in cart.items.all():
            order.items.add(item)
        cart.items.all().delete()
        messages.success(request, "done")
        return redirect("purchases")
    except Exception as e:
        messages.error(request, "error")
        return redirect("cart")

def logouts(request):
    logout(request)
    return redirect("login")


# public class Main{
#     public static void main(String[] args){
#         System.out.println("atro or ntro ")
#     }
# }