from django.urls import path

from django.contrib.auth import views as auth_views #authentication views, use 'as' to rename the views

from . import views


app_name = 'accounts'

urlpatterns = [
    path('', views.home, name = 'home'),

    path('register', views.registerPage, name = 'register'),
    path('login', views.loginPage, name = 'login'),
    path('logout', views.logoutUser, name = 'logout'),

    path('user/', views.userPage, name = 'user_page'),
    path('account/', views.account_settings, name = 'account_settings'),

    path('products/', views.products, name = 'products'),
    path('customer/<str:pk>/', views.customer, name = 'customer'),

    path('create_order/', views.createOrder, name = 'create_order'),
    path('create_multiple_order/<str:pk>', views.createMultipleOrder, name = 'create_multiple_order'),
    path('update_order/<str:pk>/', views.updateOrder, name = 'update_order'),
    path('delete/<str:pk>/', views.deleteOrder, name = 'delete_order'),

    path('create_customer/', views.createCustomer, name = 'create_customer'),
    path('update_customer/<str:pk>/', views.updateCustomer, name = 'update_customer'),
    path('delete_customer/<str:pk>/', views.deleteCustomer, name = 'delete_customer'),

    path('create_product/', views.createProduct, name = 'create_product'),
    path('update_product/<str:pk>/', views.updateProduct, name = 'update_product'),
    path('delete_product/<str:pk>/', views.deleteProduct, name = 'delete_product'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name = "accounts/password_reset.html"), name = "reset_password"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name = "accounts/password_reset_sent.html"), name = "password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = "accounts/password_reset_form.html"), name = "password_reset_confirm"),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name = "accounts/password_reset_done.html"), name = "password_reset_complete"),

]
