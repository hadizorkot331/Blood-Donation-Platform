from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import RegistrationForm, ProfileCompletionForm


def landing_page(request):
    return render(request, "users/landing-page.html")


def register(request):
    if request.method == "POST":
        form = RegistrationForm(data=request.POST)

        if form.is_valid():
            # When users register, they need to complete their profile to have full functionality.
            # Profile completion is done in a seperate view
            # Therefore, we dont save the user's registration information into the database when they register
            # Instead, the registration information and the profile are saved after completing the profile
            # This is done to avoid fragmented user and profile data in the database
            request.session["user_registration_data"] = request.POST
            return redirect("users:complete-profile")
    else:
        form = RegistrationForm()
    return render(request, "users/register.html", {"form": form})


def complete_profile(request):
    # Make sure that the user has completed registration before accessing this page
    # Also account for people trying to access the page after already registering
    if "user_registration_data" not in request.session:
        if request.user.is_authenticated:
            messages.warning(request, "Profile Already Created")
            return redirect("posts:home")
        else:
            return redirect("users:register")

    if request.method == "POST":
        form = ProfileCompletionForm(request.POST)

        if form.is_valid():
            # Add the user to the database and remove the registration information from the session
            user = UserCreationForm(request.session["user_registration_data"]).save()
            login(request, user)
            del request.session["user_registration_data"]

            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            messages.success(
                request,
                "Account Created! Join Whatsapp Group For Notifications (Navbar)",
            )
            return redirect("posts:home")
    else:
        form = ProfileCompletionForm()

    return render(
        request,
        "users/complete-profile.html",
        {"form": form},
    )


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


@login_required(login_url="/users/login")
def logout_view(request):
    logout(request)
    return redirect("users:login")
