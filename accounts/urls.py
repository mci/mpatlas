from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    # Login user/password
    (r'^login/$', 
        'django.contrib.auth.views.login', 
        {'template_name': 'accounts/login.html'}),
    
    # Logout current user
    (r'^logout/$', 
        'django.contrib.auth.views.logout', 
        {'template_name': 'accounts/logout.html'}),
    
    # Register for an account
    (r'^signup/$', 
        'accounts.views.signup', 
        {'template_name': 'accounts/signup.html',
        'email_template_name': 'accounts/signup_email.html'}),
    
    # Registration complete, but email verification pending
    (r'^signup/done/$', 
        'accounts.views.signup_done', 
        {'template_name': 'accounts/signup_done.html'}),
    
    # Email link with token for signup email confirmation
    (r'^signup/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 
        'accounts.views.signup_confirm'),
    
    # Sign up complete, email verified
    (r'^signup/complete/$', 
        'accounts.views.signup_complete', 
        {'template_name': 'accounts/signup_complete.html'}),
    
    # Change password
    (r'^password_change/$', 
        'django.contrib.auth.views.password_change', 
        {'template_name': 'accounts/password_change_form.html'}),
    
    # Password change complete
    (r'^password_change/done/$', 
        'django.contrib.auth.views.password_change_done', 
        {'template_name': 'accounts/password_change_done.html'}),
    
    # Reset/forgot password
    (r'^password_reset/$', 
        'django.contrib.auth.views.password_reset', 
        {'template_name': 'accounts/password_reset_form.html',
        'email_template_name': 'accounts/password_reset_email.html',
        'from_email': 'webrobot@marine-conservation.org',}),
    
    # Password reset complete
    (r'^password_reset/done/$', 
        'django.contrib.auth.views.password_reset_done', 
        {'template_name': 'accounts/password_reset_done.html'}),
    
    # Password reset email link with token
    (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 
        'django.contrib.auth.views.password_reset_confirm', 
        {'template_name': 'accounts/password_reset_confirm.html'}),
    
    # Password reset complete
    (r'^reset/done/$', 
        'django.contrib.auth.views.password_reset_complete', 
        {'template_name': 'accounts/password_reset_complete.html'}),
    
)
