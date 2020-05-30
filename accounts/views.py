from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm # for register
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages # for flash message
from django.contrib.auth.models import Group # for assigning register users as customer
from .models import * # import models
from .forms import OrderForm, Register, CustomerForm # for forms #Orderform Not Using
from .filters import OrderFilter # for search
from .decorators import unauthenticated_user, allowed_users, admin_only
# from django.http import HttpResponse
# Create your views here.
@login_required(login_url = 'login')
@allowed_users(['customer'])
def user_account(req):
	orders = req.user.customer.order_set.all()
	# print(orders)
	context = {
		'orders' : orders,
		'orders_delivered' : orders.filter(status='Delivered').count(),
		'orders_pending' : orders.filter(status='Pending').count(),
		'orders_total' : orders.count(),
	}
	return render(req, 'accounts/profile.html', context)

@login_required(login_url = 'login')
@allowed_users(['customer'])
def account_settings(req):
	user = req.user.customer
	if req.method == 'POST':
		form = CustomerForm(req.POST, req.FILES, instance = user)
		if form.is_valid():
			form.save()

	form = CustomerForm(instance = user)
	context = {
		'form' : form
	}
	return render(req,'accounts/settings.html', context)


@unauthenticated_user
def register(req):
	if req.method == 'POST':
		form = Register(req.POST)
		if form.is_valid():
			user = form.save()

			# Used signals for adding on group and adding user to on customer table also
			'''
			group = Group.objects.get(name = 'customer')
			user.groups.add(group)
			#for adding on customer table also
			Customer.objects.create(
				user = user,
				name = user.username,
				# name = 'test model', # we can assign model value here
				)
			'''
			

			username = form.cleaned_data.get('username')
			messages.success(req,f'Account has been created for {username}')
			return redirect('login')
	context = {
		'form' : Register
	}
	return render(req, 'accounts/register.html', context)

@unauthenticated_user
def login_page(req):
	if req.method == 'POST':
		username = req.POST.get('username')
		password = req.POST.get('password')
		login_auth = authenticate(req, username = username, password = password)
		if login_auth is not None:
			login(req, login_auth)
			return redirect('dashboard')
		else:
			messages.info(req, 'Username OR Password is Incorrect')
	return render(req, 'accounts/login.html')


def logout_user(req):
	logout(req)
	return redirect('login')
	# return render(req, 'accounts/login.html')

@login_required(login_url = 'login')
@admin_only
def home(req):
	orders = Order.objects.all()
	customers = Customer.objects.all()
	context = {
		'orders' : orders,
		'orders_delivered' : orders.filter(status='Delivered').count(),
		'orders_pending' : orders.filter(status='Pending').count(),
		'orders_total' : orders.count(),
		'customers' : customers,
	}
	return render(req, 'accounts/dashboard.html', context)
@login_required(login_url = 'login')
@allowed_users(roles=['admin'])
def products(req):
	products = Product.objects.all()
	data = {
		'products' : products
	}
	return render(req, 'accounts/products.html', data)

@login_required(login_url = 'login')
@allowed_users(roles=['admin'])
def customer(req, cust_id):
	customer = Customer.objects.get(id=cust_id)
	orders = customer.order_set.all()

	search_filter = OrderFilter(req.GET, queryset=orders)
	orders = search_filter.qs
	context = {
		'customer' : customer,
		'orders' : orders,
		'total_orders' : orders.count(),
		'search_filter' : search_filter.form,
	}
	return render(req, 'accounts/customer.html', context)

'''def create_order_single(req):
	form = OrderForm()
	if req.method == 'POST':
		# print(req.POST)
		form = OrderForm(req.POST)
		if form.is_valid():
			form.save()
			return redirect('/')
			
	context = {
		'form':form,
	}
	return render(req, 'accounts/order_form.html', context)'''
@login_required(login_url = 'login')
@allowed_users(roles=['admin'])
def create_order(request, cust_id):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10 )
	customer = Customer.objects.get(id=cust_id)
	formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)
	#form = OrderForm(initial={'customer':customer})
	if request.method == 'POST':
		#print('Printing POST:', request.POST)
		#form = OrderForm(request.POST)
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {'form':formset, 'customer':customer}
	return render(request, 'accounts/order_form.html', context)

@login_required(login_url = 'login')
@allowed_users(roles=['admin'])
def update_order(req, u_id):
	fetch_order = Order.objects.get(id=u_id)
	form = OrderForm(instance=fetch_order)
	if req.method == 'POST':
		form = OrderForm(req.POST, instance=fetch_order)
		if form.is_valid():
			form.save()
			return redirect('/')

	context = {
		'form':formset,
	}
	return render(req, 'accounts/order_form.html', context)

@login_required(login_url = 'login')
@allowed_users(roles=['admin'])
def delete_order(req, del_id):
	fetch_order = Order.objects.get(id=del_id)
	if req.method == 'POST':
		fetch_order.delete()
		return redirect('/')
	context = {
		'item' : fetch_order
	}
	return render(req, 'accounts/delete.html', context)