from django.http.response import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
	def wrapper_func(req, *args, **kwargs):
		if req.user.is_authenticated:
			return redirect('dashboard')
		else:
			return view_func(req, *args, **kwargs)

	return wrapper_func

def allowed_users(roles = []):
	def decorator(view_func):
		def wrapper_func(req, *args, **kwargs):
			# print('working',roles)
			group = None
			if req.user.groups.exists():
				group = req.user.groups.all()[0].name
			if group in roles:
				return view_func(req, *args, **kwargs)
			else:
				return HttpResponse('You are not authorized to view this page.')
		return wrapper_func
	return decorator

def admin_only(view_func):
	def wrapper_func(req, *args, **kwargs):
		# print('working',roles)
		group = None
		if req.user.groups.exists():
			group = req.user.groups.all()[0].name
		if group in 'customer':
			return redirect('user_account')
		if group in 'admin':
			return view_func(req, *args, **kwargs)
	return wrapper_func
