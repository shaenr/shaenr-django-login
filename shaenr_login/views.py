from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import user_passes_test
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.db.models import Q

from .models import MyUser
from .forms import UserCreationForm
from .tokens import account_activation_token


# Create your views here.
def index_page(request):
    return render(request, "shaenr_login/index.html")


@user_passes_test(lambda user: user.is_staff)
def listing(request):
    data = {
        "users": MyUser.objects.all(),
    }

    return render(request, "listing.html", data)


def view_user(request, _id):
    user = get_object_or_404(MyUser, id=_id)
    data = {
        "user": user,
    }

    return render(request, "view_user.html", data)


def see_request(request):
    text = f"""
        Some attributes of the HttpRequest object:

        scheme: {request.scheme}
        path:   {request.path}
        method: {request.method}
        GET:    {request.GET}
        user:   {request.user}
        
        username:     {request.user.email}
        is_anonymous: {request.user.is_anonymous}
        is_staff:     {request.user.is_staff}
        is_superuser: {request.user.is_superuser}
        is_active:    {request.user.is_active}
    """

    return HttpResponse(text, content_type="text/plain")


def _send_verification_email(request, user=None, form=None, **kwargs):
    if user is not None:
        current_site = get_current_site(request)
        # ADMIN_EMAIL = f"verify@{current_site.domain}"
        # if not ADMIN_EMAIL.endswith('.com'):
        #     ADMIN_EMAIL += ".com"
        ADMIN_EMAIL = "verifyTest@djangoLoginTest.org"
        mail_subject = f"{current_site.domain}: Activate your account"
        message = render_to_string('shaenr_login/email_verify.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user)
        })
        to_email = form.cleaned_data.get('email')
        send_mail(mail_subject, message, ADMIN_EMAIL, [to_email])


def register(request):
    User = get_user_model()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.filter(
                email__iexact=email
            ).first()
            if not user:
                user = form.save(commit=False)
                user.is_active = False
                user.save()
                _send_verification_email(
                    request, user=user, form=form
                )
                return HttpResponse(
                    'Please confirm your email address to complete the registration'
                )
            elif user and not user.email_verified:
                _send_verification_email(
                    request, user=user, form=form
                )
                return HttpResponse(
                    f'{user.email} already exists... Check your email to verify.'
                )
        else:
            return redirect(reverse('register'))

    elif request.method == "GET":
        form = UserCreationForm()
        return render(
            request, 'shaenr_login/register.html', {
                'form': form
            }
        )


def verify_email(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')