from email import message
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render

from .forms import RegistrationForm, ProfileCompletionForm


def landing_page(request):
    return render(request, "users/landing-page.html")


# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegistrationForm(data=request.POST)

        if form.is_valid():
            request.session["user_registration_data"] = request.POST
            return redirect("users:complete-profile")
    else:
        form = RegistrationForm()
    return render(request, "users/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            login(request, form.get_user())

            if "next" in request.POST:
                return redirect(request.POST.get("next", "/"))
            else:
                return redirect("posts:home")
    else:
        form = AuthenticationForm()

    return render(request, "users/login.html", {"form": form})


def complete_profile(request):
    if "user_registration_data" not in request.session:
        if request.user.is_authenticated:
            messages.warning(request, "Profile Already Created")
            return redirect("posts:home")
        else:
            return redirect("users:register")

    if request.method == "POST":
        form = ProfileCompletionForm(request.POST)

        if form.is_valid():
            user = UserCreationForm(request.session["user_registration_data"]).save()
            login(request, user)
            del request.session["user_registration_data"]

            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.warning(request, "Join Whatsapp Group For Notifications (Navbar)")
            return redirect("posts:home")
    else:
        form = ProfileCompletionForm()

    return render(
        request,
        "users/complete-profile.html",
        {"form": form},
    )


@login_required(login_url="/users/login")
def logout_view(request):
    logout(request)
    return redirect("users:login")
