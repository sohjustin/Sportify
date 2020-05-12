from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *
from .filters import *
from .decorators import *
# Create your views here.


@unathenticated_user
def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            messages.success(request, 'Account was created for ' + username)

            return redirect('accounts:login')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)

@unathenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('accounts:home')
        else:
            messages.info(request, "Username OR Password is incorrect")

    context = {}
    return render(request, 'accounts/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('accounts:login')

@login_required(login_url = 'accounts:login')
@admin_only
def home(request):
    total_orders = Order.objects.all().count()
    pending_orders = Order.objects.filter(status = 'Pending').count()
    orders_delivered = Order.objects.filter(status = 'Delivered').count()

    customers = Customer.objects.all()
    orders = Order.objects.all()
    return render(request, 'accounts/dashboard.html', {'total_orders': total_orders,
                                                    'pending_orders': pending_orders,
                                                    'orders_delivered': orders_delivered,
                                                    'customers': customers,
                                                    'orders' : orders })


@login_required(login_url = 'accounts:login')
@allowed_users(allowed_roles = ['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    customer = request.user.customer
    total_orders = orders.count()
    pending_orders = orders.filter(status = 'Pending').count()
    orders_delivered = orders.filter(status = 'Delivered').count()
    context = {'orders': orders, 'total_orders': total_orders, 'pending_orders': pending_orders,
            'orders_delivered': orders_delivered, 'customer' :customer}
    return render(request, 'accounts/user.html', context)


@login_required(login_url = 'accounts:login')
@allowed_users(allowed_roles = ['customer'])
def account_settings(request):
    customer = request.user.customer    #get customer information
    form = CustomerForm(instance = customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance = customer) #as you want to take in files too, need to include 'request.FILES'
        if form.is_valid():
            form.save()
    context = {'form': form}
    return render(request, 'accounts/account_settings.html', context)


@login_required(login_url = 'accounts:login')
@allowed_users(allowed_roles = ['admin', 'customer'])
def products(request):
    products = Product.objects.all()
    myFilter = ProductFilter(request.GET, queryset=products)
    return render(request, 'accounts/products.html', {'products': products, 'myFilter': myFilter} )


@login_required(login_url = 'accounts:login')
@allowed_users(allowed_roles = ['admin'])
def customer(request, pk):
    customers = Customer.objects.get(id=pk)
    orders = customers.order_set.all()
    count_orders = orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs  #qs stands for queryset

    return render(request, 'accounts/customer.html', {'customers': customers,
                                                    'orders': orders,
                                                    'count_orders': count_orders,
                                                    'myFilter': myFilter})
@login_required(login_url = 'accounts:login')
@allowed_users(allowed_roles = ['admin', 'customer'])
def createOrder(request):
    form = OrderForm()
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'formset': form}

    return render(request, 'accounts/order_form.html', context)

@login_required(login_url = 'accounts:login')
@allowed_users(allowed_roles = ['admin', 'customer'])
def createMultipleOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields = ('product', 'status'), extra = 3)

    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance = customer)

    if request.method == 'POST':
        # form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST, instance = customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')
    context = {'formset': formset}

    return render(request, 'accounts/order_form.html', context)

@login_required(login_url = 'accounts:login')
@allowed_users(allowed_roles = ['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)

    if request.method == 'POST':
        form = OrderForm(request.POST, instance = order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'accounts/order_form.html', context)


@login_required(login_url = 'accounts:login')
@allowed_users(allowed_roles = ['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)

    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'item': order}
    return render(request, 'accounts/delete.html', context)


@login_required(login_url = 'accounts:login')
@allowed_users(allowed_roles = ['admin'])
def createCustomer(request):
    form = CustomerForm
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form' : form}
    return render(request, 'accounts/customer_form.html', context)


@login_required(login_url = 'accounts:login')
@allowed_users(allowed_roles = ['admin'])
def updateCustomer(request, pk):
    customer = Customer.objects.get(id=pk)
    form = CustomerForm(instance = customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, instance = customer)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form' : form}
    return render(request, 'accounts/customer_form.html', context)


@login_required(login_url = 'accounts:login')
@allowed_users(allowed_roles = ['admin'])
def deleteCustomer(request, pk):
    customer = Customer.objects.get(id=pk)

    if request.method == 'POST':
        customer.delete()
        return redirect('/')

    context = {'item': customer}
    return render(request, 'accounts/delete.html', context)





@login_required(login_url = 'accounts:login')
@allowed_users(allowed_roles = ['admin'])
def createProduct(request):
    form = ProductForm
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:products')

    context = {'form' : form}
    return render(request, 'accounts/product_form.html', context)


@login_required(login_url = 'accounts:login')
@allowed_users(allowed_roles = ['admin'])
def updateProduct(request, pk):
    product = Product.objects.get(id=pk)
    form = ProductForm(instance = product)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance = product)
        if form.is_valid():
            form.save()
            return redirect('accounts:products')

    context = {'form' : form}
    return render(request, 'accounts/product_form.html', context)


@login_required(login_url = 'accounts:login')
@allowed_users(allowed_roles = ['admin'])
def deleteProduct(request, pk):
    product = Product.objects.get(id=pk)

    if request.method == 'POST':
        product.delete()
        return redirect('accounts:products')

    context = {'item': product}
    return render(request, 'accounts/delete.html', context)
