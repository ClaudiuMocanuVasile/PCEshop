from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import ResetPasswordForm, ResetPasswordConfirmForm



urlpatterns = [

    # Main content

    path('', views.shop, name = "shop"),
    path('shop/', views.shop, name = "shop"),
    path('product/', views.product, name = "product"),

	# Privacy and cookie policy

    path('privacy_policy/', views.privacy_policy, name = "privacy_policy"),
    path('cookie_policy/', views.cookie_policy, name = "cookie_policy"),

    # Cart and checkout

    path('cart/', views.cart, name = "cart"),
    path('update_product/', views.updateProduct, name = "update_product"),
    path('process_order/', views.processOrder, name = "process_order"),
    path('checkout/', views.checkout, name = "checkout"),

    # Login, logout and registration

    path('login_page/', views.login_page, name = "login_page"),
    path('registration_page/', views.registration_page, name = "registration_page"),
    path('logout/', views.Logout, name = "logout"),

	# Password reset

    path('reset_password/', 
		auth_views.PasswordResetView.as_view(
		    template_name = "shop/reset_password.html", 
		    form_class = ResetPasswordForm
        ), 
		name = "reset_password"
	),

    path('reset_password_done/', 
		auth_views.PasswordResetDoneView.as_view(
            template_name = "shop/reset_password_done.html"
        ), 
	    name = "password_reset_done"
	),

    path('reset/<uidb64>/<token>/', 
		auth_views.PasswordResetConfirmView.as_view(
            template_name = "shop/reset_password_confirm.html",
            form_class = ResetPasswordConfirmForm
        ), 
		name = "password_reset_confirm"
	),

    path('reset_password_complete/', 
		auth_views.PasswordResetCompleteView.as_view(
            template_name = "shop/reset_password_complete.html"
        ), 
		name = "password_reset_complete"
	),

    path('reset/<uidb64>/set-password/',
		views.reset_back, 
		name = "reset_back"
	),

    path('change_password/', 
        auth_views.PasswordChangeView.as_view(
            template_name = "shop/change_password.html"
        ), 
        name = "change_password"
    ),

    # Profile and delete account

    path('profile/', views.profile_page, name = "profile_page"),
    path('delete/', views.Delete, name = "delete"),

]
