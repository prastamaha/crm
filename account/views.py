from django.shortcuts import render, redirect
from django.forms import inlineformset_factory
from .models import *
from .forms import *
from .filters import *

from django.contrib.auth.models import Group

# authentication
from django.contrib.auth import authenticate, login, logout

# messages
from django.contrib import messages

# decorators
from django.contrib.auth.decorators import login_required
from .decorators import *

@login_required(login_url='login')
@allowed_users(allowed_group=['admin'])
def home(request):
    
    customers = Customer.objects.all()
    orders = Order.objects.all()
    order_total = orders.count()
    order_delivered = orders.filter(status='delivered').count()
    order_pending = orders.filter(status='pending').count()

    context = {
        'customers': customers,
        'orders': orders,
        'order_total': order_total,
        'order_delivered': order_delivered,
        'order_pending': order_pending,
    }
    return render(request, 'account/home.html', context)

@login_required(login_url='login')
@allowed_users(allowed_group=['admin'])
def products(request):
    products = Product.objects.all()
    
    context = {'products': products}
    return render(request, 'account/products.html', context)

@login_required(login_url='login')
@allowed_users(allowed_group=['admin'])
def customers(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    
    filter = OrderFilter(request.GET, queryset=orders)
    orders = filter.qs

    context = {
        'customer': customer,
        'orders':orders,
        'filter': filter,
    }
    return render(request, 'account/customers.html', context)

@login_required(login_url='login')
@allowed_users(allowed_group=['admin'])
def create_product(request):
    form = ProductForm()

    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('products')
    
    context = {'form':form}
    return render(request, 'account/create_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_group=['admin','customer'])
def create_order(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status', 'note'), extra=1, can_delete=False)
    
    customer = Customer.objects.get(id=pk)
    
    form = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    if request.method == 'POST':
        form = OrderFormSet(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'account/create_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_group=['admin','customer'])
def update_order(request, pk):
    
    order = Order.objects.get(id=pk)

    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'account/create_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_group=['admin','customer'])
def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    order.delete()
    if request.user.groups.filter(name='customer').exists():
        return redirect('user_dashboard')
    return redirect('home')

@unauthenticated_user
def registerPage(request):
    form = UserRegistrationForm()

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()

            # kode dibawah sudah dihandle oleh django signal di signals.py
            # user = form.save()
            
            # add created user to customer group
            # group = Group.objects.get(name='customer')
            # user.groups.add(group)

            # add created user to a customer user object
            # Customer.objects.create(
            #     user=user,
            #     name=user.username,
            # )

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account "{username}" was created! please login with your account.')
            return redirect('login')

    context = {'form':form}
    return render(request, 'account/register.html', context)

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'username or password is incorrect')

    context = {}
    return render(request, 'account/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect('login')

@login_required
@allowed_users(allowed_group=['admin','customer'])
def userDashboard(request):
    orders = request.user.customer.order_set.all()
    orders_delivered = orders.filter(status='delivered').count()
    orders_pending = orders.filter(status='pending').count()
    customer = request.user.customer

    context = {
        'orders':orders,
        'orders_delivered':orders_delivered,
        'orders_pending':orders_pending,
        'customer':customer,
    }
    return render(request, 'account/user.html', context)

def userProfile(request):
    user = request.user.customer
    form = CustomerForm(instance=user)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    
    context = {'form':form}
    return render(request, 'account/profile.html', context)

def customerRegis(request):

    form = CustomerRegistration()
    
    if request.method == 'POST':
        form = CustomerRegistration(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request, 'account/create_form.html', context)