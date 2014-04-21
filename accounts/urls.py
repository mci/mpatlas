from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Login user/password
    url(r'^login/$', 
        'django.contrib.auth.views.login', 
        {'template_name': 'accounts/login.html'},
        name='login'),
    
    # Logout current user
    url(r'^logout/$', 
        'django.contrib.auth.views.logout', 
        {'template_name': 'accounts/logout.html'},
        name='logout'),
    
    # Register for an account
    url(r'^signup/$', 
        'accounts.views.signup', 
        {'template_name': 'accounts/signup.html',
        'email_template_name': 'accounts/signup_email.html'},
        name='signup'),
    
    # Registration complete, but email verification pending
    url(r'^signup/done/$', 
        'accounts.views.signup_done', 
        {'template_name': 'accounts/signup_done.html'},
        name='signup_done'),
    
    # Email link with token for signup email confirmation
    url(r'^signup/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 
        'accounts.views.signup_confirm',
        name='signup_confirm'),
    
    # Sign up complete, email verified
    url(r'^signup/complete/$', 
        'accounts.views.signup_complete', 
        {'template_name': 'accounts/signup_complete.html'},
        name='signup_complete'),
    
    # Change password
    url(r'^password_change/$', 
        'django.contrib.auth.views.password_change', 
        {'template_name': 'accounts/password_change_form.html'},
        name='password_change'),
    
    # Password change complete
    url(r'^password_change/done/$', 
        'django.contrib.auth.views.password_change_done', 
        {'template_name': 'accounts/password_change_done.html'},
        name='password_change_done'),
    
    # Reset/forgot password
    url(r'^password_reset/$', 
        'django.contrib.auth.views.password_reset', 
        {'template_name': 'accounts/password_reset_form.html',
        'email_template_name': 'accounts/password_reset_email.html',
        'from_email': 'webrobot@marine-conservation.org',},
        name='password_reset'),
    
    # Password reset complete
    url(r'^password_reset/done/$', 
        'django.contrib.auth.views.password_reset_done', 
        {'template_name': 'accounts/password_reset_done.html'},
        name='password_reset_done'),
    
    # Password reset email link with token
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 
        'django.contrib.auth.views.password_reset_confirm', 
        {'template_name': 'accounts/password_reset_confirm.html'},
        name='password_reset_confirm'),
    
    # Password reset complete
    url(r'^reset/done/$', 
        'django.contrib.auth.views.password_reset_complete', 
        {'template_name': 'accounts/password_reset_complete.html'},
        name='password_reset_complete'),
    
)
