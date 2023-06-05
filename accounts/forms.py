from django.contrib.auth import get_user_model
from django_countries.fields import CountryField
from django_countries import countries
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator

try:
    from django.contrib.sites.models import get_current_site
except ImportError:
    from django.contrib.sites.shortcuts import get_current_site
from django.template import Context, loader
from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils.http import int_to_base36

from accounts.models import TITLE_CHOICES

User = get_user_model()


class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and password.
    """

    username = forms.RegexField(
        label=_("Username"),
        max_length=30,
        regex=r"^[\w.@+-]+$",
        help_text=_(
            "Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        error_messages={
            "invalid": _(
                "This value may contain only letters, numbers and @/./+/-/_ characters."
            )
        },
    )
    password1 = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."),
    )
    email1 = forms.EmailField(
        label="Email",
        max_length=75,
        help_text="A confirmation email will be sent to this address.",
    )
    # email2 = forms.EmailField(label="Email confirmation", max_length=75,
    #     help_text = "Enter your email address again.")
    title = forms.ChoiceField(label=_("Title"), choices=TITLE_CHOICES)
    first_name = forms.CharField(label=_("First Name"), max_length=30)
    last_name = forms.CharField(label=_("Last Name"), max_length=30)
    affiliation = forms.CharField(
        label=_("Affiliation/Organization"), max_length=300, required=False
    )
    country = forms.ChoiceField(label=_("Country"), choices=countries, initial="US")

    class Meta:
        model = User
        fields = (
            "username",
            "password1",
            "password2",
            "email1",
            "title",
            "first_name",
            "last_name",
            "affiliation",
            "country",
        )

    def __init__(self, *args, **kwargs):
        self.user_cache = None
        super(UserCreationForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(_("A user with that username already exists."))

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1", "")
        password2 = self.cleaned_data["password2"]
        if password1 != password2:
            raise forms.ValidationError(_("The two password fields didn't match."))
        return password2

    def clean_email1(self):
        email1 = self.cleaned_data["email1"]
        users_found = User.objects.filter(email__iexact=email1)
        if len(users_found) >= 1:
            raise forms.ValidationError("A user with that email already exist.")
        return email1

    def clean_email2(self):
        email1 = self.cleaned_data.get("email1", "")
        email2 = self.cleaned_data["email2"]
        if email1 != email2:
            raise forms.ValidationError("The two email fields didn't match.")
        return email2

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["email1"]
        user.is_active = True
        user.is_staff = False
        user.is_superuser = False
        if commit:
            user.save()
        # UserProfile is created by post_save signal on User
        # profile = user.get_profile()
        user = User.objects.get(pk=user.pk)  # refresh to get auto-created profile
        profile = user.userprofile
        profile.title = self.cleaned_data["title"]
        profile.affiliation = self.cleaned_data["affiliation"]
        profile.country = self.cleaned_data["country"]
        profile.save()
        # Send mail confirmation here
        # t = loader.get_template(email_template_name)
        # c = {
        #     'email': user.email,
        #     'domain': domain,
        #     'site_name': site_name,
        #     'uid': int_to_base36(user.id),
        #     'user': user,
        #     'token': token_generator.make_token(user),
        #     'protocol': use_https and 'https' or 'http',
        #     }
        # send_mail("Confirmation link sent on %s" % site_name,
        #           t.render(Context(c)), 'peyman.gohari@gmail.com', [user.email])
        self.user_cache = user
        return user
