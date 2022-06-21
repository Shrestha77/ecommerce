from datetime import datetime
from tempfile import template
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout

from .forms import ContactForm, UserCreationForm, UserProfileUpdateForm
from .decorators import unauthenticated_user
from django.contrib.auth.decorators import login_required

from . models import Product, Customer, Order, OrderItem, ShippingAddress
from math import ceil
import json
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView, PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin

# Create your views here.


@unauthenticated_user
def register(request):
    template = 'users/create.html'
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('first_name')

            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(
                user=user,
                name=user.first_name,
                email=user.email,
                phone=user.contact,
            )

            messages.success(
                request, 'Account was created for ' + username)

            return redirect('user.login')
    context = {'form': form}
    return render(request, template, context)


@unauthenticated_user
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('ShopHome')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'users/login.html', context)


def user_logout(request):
    logout(request)
    return redirect('ShopHome')


def index(request):
    products = Product.objects.all()
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item["category"] for item in catprods}
    for cat in cats:
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod, range(1, nSlides), nSlides])
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    context = {'allProds': allProds, 'order': order}
    template = "shop/index.html"
    return render(request, template, context)


def searchMatch(query, item):
    if query in item.description.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False


def search(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    query = request.GET.get('search')
    prodtemp = Product.objects.all()
    prod = [item for item in prodtemp if searchMatch(query.lower(), item)]
    context = {'prod': prod, "msg": "", 'order': order}
    if len(query) == 0:
        context = {'msg': "Please make sure to enter relevant search query"}
    template = 'shop/search.html'
    return render(request, template, context)


def about(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    context = {'order': order}
    template = 'shop/about.html'
    return render(request, template, context)


def contact(request):
    form = ContactForm()
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            context = {'form': form}
            template = 'shop/contact.html'
            return render(request, template, context)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    context = {'form': form, 'order': order}
    template = 'shop/contact.html'
    return render(request, template, context)


def tracker(request):
    context = {}
    template = 'shop/tracker.html'
    return render(request, template, context)


def productView(request, myid):
    products = Product.objects.all()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    product = Product.objects.filter(id=myid)
    context = {'product': product[0], 'order': order, 'products': products}
    template = 'shop/productview.html'
    return render(request, template, context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    context = {'items': items, 'order': order}
    template = 'shop/checkout.html'
    return render(request, template, context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    context = {'items': items, 'order': order}
    template = 'shop/cart.html'
    return render(request, template, context)


def updateitem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('ProductId:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderItem.qunatity = (orderItem.qunatity + 1)
    elif action == 'remove':
        orderItem.qunatity = (orderItem.qunatity - 1)

    orderItem.save()

    if orderItem.qunatity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)


def processOrder(request):
    transaction_id = datetime.now().timestamp()
    data = json.loads(request.body)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id
        if total == order.get_cart_total:
            order.complete = True
            order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                district=data['shipping']['district'],
            )
    else:
        print('user is not loggesd in')

    return JsonResponse('payment complete', safe=False)


def clearCart(request):
    orderItem = OrderItem.objects.all()
    orderItem.delete()
    return redirect('cart')


@login_required(login_url='user.login')
def profileShow(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0, 'shipping': False}
    context = {'user': request.user, 'order': order}
    template = 'users/profile.html'
    return render(request, template, context)


@login_required(login_url='user.login')
def profileEdit(request):
    template = 'users/edit.html'
    context = {'user': request.user}
    return render(request, template, context)


@login_required(login_url='user.login')
def profileUpdate(request):
    template = 'users/edit.html'
    form = UserProfileUpdateForm()
    context = {'user': request.user}
    if request.method == "POST":
        obj_form_data = UserProfileUpdateForm(
            request.POST, request.FILES, instance=request.user)
        if obj_form_data.is_valid():
            obj_form_data.save()
            context.setdefault('success', 'Profile updated Successfuly')
            return render(request, template, context)
    else:
        return render(request, template, context)



class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'password/changepassword.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('user.profile')



class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'password/password_reset.html'
    email_template_name = 'password/password_reset_email.html'
    subject_template_name = 'password/password_reset_subject.txt'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('ShopHome')
