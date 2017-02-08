from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
try:
    from django.contrib.sites.models import get_current_site
except ImportError:
    from django.contrib.sites.shortcuts import get_current_site
from django.template import Context, loader
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.utils.http import int_to_base36
from django.contrib.auth import authenticate, login

from django.contrib.auth.models import User
from django.shortcuts import render_to_response, render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from accounts.forms import UserCreationForm
from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.conf import settings
from django.utils.http import urlquote, base36_to_int
from django.contrib.sites.models import Site

#from django.views.decorators.csrf import csrf_protect

User = get_user_model()

#@csrf_protect
def signup(request, template_name='accounts/signup.html', 
           email_template_name='accounts/signup_email.html',
           signup_form=UserCreationForm,
           token_generator=default_token_generator,
           post_signup_redirect=None,
           redirect_field_name='next'):
    redirect_to = request.POST.get(redirect_field_name, request.GET.get(redirect_field_name, ''))
    if post_signup_redirect is None:
        post_signup_redirect = reverse('accounts.views.signup_done')
    if request.method == "POST":
        form = signup_form(request.POST)
        if form.is_valid():
            opts = {}
            # options to facilitate confirmation emailing by signup form in forms.py
            # opts['use_https'] = request.is_secure()
            # opts['token_generator'] = token_generator
            # opts['email_template_name'] = email_template_name
            # if not Site._meta.installed:
            #     opts['domain_override'] = RequestSite(request).domain
            newuser = form.save(**opts)
            # user = form.get_user()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
            if not redirect_to:
                if (post_signup_redirect is None):
                    post_signup_redirect = reverse('accounts.views.signup_done')
                else:
                    redirect_to = post_signup_redirect
            return HttpResponseRedirect(redirect_to)
    else:
        form = signup_form()
    return render(request, template_name, {
            'form': form,
            redirect_field_name: redirect_to,
        })

def signup_done(request, template_name='accounts/signup_done.html'):
    return render(request, template_name)

def signup_confirm(request, uidb36=None, token=None,
                   token_generator=default_token_generator,
                   post_signup_redirect=None):
    assert uidb36 is not None and token is not None #checked par url
    if post_signup_redirect is None:
        post_signup_redirect = reverse('accounts.views.signup_complete')
    try:
        uid_int = base36_to_int(uidb36)
    except ValueError:
        raise Http404

    user = get_object_or_404(User, id=uid_int)
    context_instance = RequestContext(request)

    if token_generator.check_token(user, token):
        context_instance['validlink'] = True
        user.is_active = True
        user.save()
    else:
        context_instance['validlink'] = False
    return HttpResponseRedirect(post_signup_redirect)

def signup_complete(request, template_name='accounts/signup_complete.html'):
    return render(request, template_name, {'login_url': settings.LOGIN_URL}))
