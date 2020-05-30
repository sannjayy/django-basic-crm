from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('', views.home, name="dashboard"),
    path('products/', views.products, name="product"),
    path('customer/<str:cust_id>/', views.customer, name="customer"),
    path('register/', views.register, name="register"),
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_user, name="logout"),

    path('user_account/', views.user_account, name="user_account"),
    path('settings/', views.account_settings, name="account_settings"),
    
    path('create_order/<str:cust_id>/', views.create_order, name="createOrder"),
    path('update_order/<str:u_id>/', views.update_order, name="updateOrder"),
    path('delete_order/<str:del_id>/', views.delete_order, name="deleteOrder"),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name = 'accounts/password_recover/password_reset.html'), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name = 'accounts/password_recover/password_reset_sent.html'), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'accounts/password_recover/password_reset_form.html'), name="password_reset_confirm"),
    path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'accounts/password_recover/password_reset_done.html'), name="password_reset_complete"),
    ]

'''
For Reset Password
1 - Submit email form                         //PasswordResetView.as_view()
2 - Email sent success message                //PasswordResetDoneView.as_view()
3 - Link to password Rest form in email       //PasswordResetConfirmView.as_view()
4 - Password successfully changed message     //PasswordResetCompleteView.as_view()
'''    