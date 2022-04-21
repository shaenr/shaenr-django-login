from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib.auth.decorators import user_passes_test, login_required
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth.views import PasswordResetView as BasePasswordResetView
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.contrib.auth import update_session_auth_hash
from django.contrib.sites.models import Site

from .models import MyUser
from .forms import (
    UserCreationForm,
    PasswordResetForm,
    PasswordResetRequestForm
)
from .tokens import account_activation_token, password_reset_token


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


@user_passes_test(lambda user: user.is_staff)
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


# THIS IS NOT A VIEW, CONSIDER MOVING TO NEW FILE
def _send_verification_email(request, user=None, **kwargs):
    if user is not None:
        current_site = get_current_site(request)
        # ADMIN_EMAIL = f"verify@{current_site.domain}"
        # if not ADMIN_EMAIL.endswith('.com'):
        #     ADMIN_EMAIL += ".com"
        ADMIN_EMAIL = "noreply@testing.org"
        mail_subject = f"{current_site.domain}: Activate your account"
        message = render_to_string('shaenr_login/email_verify.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user)
        })
        to_email = user.email
        send_mail(mail_subject, message, ADMIN_EMAIL, [to_email])


@require_http_methods(["GET", "POST"])
def register(request):
    if not request.user.is_authenticated:
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
                    _send_verification_email(request, user=user)
                    return HttpResponse(
                        'Please confirm your email address to complete the registration'
                    )
                elif user and not user.email_verified:
                    _send_verification_email(request, user=user)
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
    else:
        return redirect(reverse("index"))


@login_required()
def get_verified(request):
    if request.user.email_verified:
        return redirect(reverse("index"))
    else:
        _send_verification_email(request, user=request.user)
        return redirect(reverse("index"))


@require_http_methods(["GET"])
def verify_email(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if not request.user.email_verified and user is not None \
            and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_verified = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
        # return redirect(reverse("index"))
        # TODO convert this to message
    else:
        return HttpResponse('Activation link is invalid!')
        # return redirect(reverse("index"))
        # TODO convert this to message


# @unauthenticated_required(home_url='/', redirect_field_name='')
@require_http_methods(["GET", "POST"])
def password_reset(request):
    msg = ""
    UserModel = get_user_model()
    if request.method == "POST":
        form = PasswordResetRequestForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            query = UserModel.objects.filter(email=email)
            site = get_current_site()

            if len(query) > 0:
                user = query.first()
                user.is_active = False
                user.forgot_password = True
                user.save()

                # Consider making helper function for _send_reset_password_email
                message = render_to_string('account/password_reset_mail.html', {
                    'user': user,
                    'protocol': 'http',
                    'domain': site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': password_reset_token.make_token(user),
                })
                to_email = user.email
                mail_subject = f"{site.domain}: Reset Your Password"
                ADMIN_EMAIL = "noreply@testing.org"
                send_mail(mail_subject, message, ADMIN_EMAIL, [to_email])

                msg = "If this mail address is known to us, an email will be sent to your account.'"
        else:
            return render(request, 'registration/password_reset_form.html', {
                'form': form
            })

    return render(request, 'registration/password_reset_form.html', {
        'form': PasswordResetRequestForm,
        'msg': msg
    })


@require_http_methods(["GET", "POST"])
def password_reset_confirm(request, uidb64, token):
    if request.method == 'POST':
        UserModel = get_user_model()
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = UserModel.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist) as e:
            # messages.add_message(request, messages.WARNING, str(e))
            user = None

        if user is not None and password_reset_token.check_token(user, token):
            form = PasswordResetForm(user=user, data=request.POST)
            if form.is_valid():
                form.save()
                update_session_auth_hash(request, form.user)

                user.is_active = True
                user.forgot_password = False
                user.save()
                # messages.add_message(request, messages.SUCCESS, 'Password reset successfully.')
                return redirect('login')
            else:

                # messages.add_message(request, messages.WARNING, 'Password could not be reset.')
                return render(
                    request, 'registration/password_reset_confirm.html', {
                        'form': form,
                        'uid': uidb64,
                        'token': token
                })
        else:
            pass
            # messages.add_message(request, messages.WARNING, 'Password reset link is invalid.')
            # messages.add_message(request, messages.WARNING, 'Please request a new password reset.')

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserModel.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist) as e:
        # messages.add_message(request, messages.WARNING, str(e))
        user = None

    if user is not None and password_reset_token.check_token(user, token):
        return render(request, 'registration/password_reset_confirm.html', {
            'form': PasswordResetForm(user),
            'uid': uidb64,
            'token': token
        })
    else:
        pass
        # messages.add_message(request, messages.WARNING, 'Password reset link is invalid.')
        # messages.add_message(request, messages.WARNING, 'Please request a new password reset.')

    return redirect('index')

# Not currently using...
# class PasswordResetView(BasePasswordResetView):
#     # TODO Make the unauthenticated password reset only reset a
#     # provided email address if that address has email_verified property.
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)

