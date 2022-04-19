from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import MyUser
from django.contrib.auth.decorators import user_passes_test

from django.contrib.auth import login

from .forms import UserCreationForm

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


def register(request):
    if request.method == "GET":
        return render(
            request, "shaenr_login/register.html",
            {"form": UserCreationForm}
        )
    elif request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("index"))
