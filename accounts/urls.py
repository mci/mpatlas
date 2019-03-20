from django.conf.urls import url, include
from django.urls import path, re_path
from django.contrib.auth.views import (LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView)

from accounts.views import signup, signup_done, signup_confirm, signup_complete

urlpatterns = [
    # Login user/password
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    # Logout current user
    path('logout/', LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    
    # Register for an account
    path('signup/', 
        signup, 
        {'template_name': 'accounts/signup.html',
        'email_template_name': 'accounts/signup_email.html'},
        name='signup'),
    
    # Registration complete, but email verification pending
    path('signup/done/', 
        signup_done, 
        {'template_name': 'accounts/signup_done.html'},
        name='signup_done'),

    # Email link with token for signup email confirmation
    re_path(r'^signup/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 
        signup_confirm,
        name='signup_confirm'),

    # Sign up complete, email verified
    path('signup/complete/', 
        signup_complete, 
        {'template_name': 'accounts/signup_complete.html'},
        name='signup_complete'),

    # Change password
    path('password_change/', 
        PasswordChangeView.as_view(template_name='accounts/password_change_form.html'),
        name='password_change'),

    # Password change complete
    path('password_change/done/', 
        PasswordChangeDoneView.as_view(template_name='accounts/password_change_done.html'),
        name='password_change_done'),

    # Reset/forgot password
    path('password_reset/', 
        PasswordResetView.as_view(template_name='accounts/password_reset_form.html', email_template_name='accounts/password_reset_email.html', from_email='webrobot@marine-conservation.org'),
        name='password_reset'),

    # Password reset complete
    path('password_reset/done/', 
        PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),
        name='password_reset_done'),

    # Password reset email link with token
    path('reset/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),
        name='password_reset_confirm'),

    # Password reset complete
    path('reset/done/',
        PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), 
        name='password_reset_complete'),
]
