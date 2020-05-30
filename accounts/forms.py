from django.forms import ModelForm # for Order Form
from django.contrib.auth.forms import UserCreationForm # for register
from django.contrib.auth.models import User # for register / fetching all users
from django import forms # for Register
from .models import Order, Customer # for order form



class OrderForm(ModelForm):
	class Meta:
		model = Order
		fields = '__all__'
		# fields = ['customer', 'product']

class Register(UserCreationForm):
	class Meta:
		model = User
		fields = ['email','username','password1','password2']

class CustomerForm(ModelForm):
	class Meta:
		model = Customer
		fields = '__all__'
		exclude = ['user']
		