import sys
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .whatsappGroup import getinvitelink
from .notifications import notify_compatible_users, send_whatsapp_message
from .models import Post
from .forms import PostForm

sys.path.append("..")
from constants import (
    HOSPITAL_CAZAS,
    CAZA_HOSPITALS,
    DONORS_TO_RECIPIENTS,
    HOSPITAL_LOCATION_DATA,
    DONORS_OF,
)


@login_required(login_url="/users/login/")
def home(request):
    user_blood_type = request.user.profile.blood_type
    user_caza = request.user.profile.caza
    posts = (
        Post.objects.filter(fullfilled=False)
        .filter(blood_type__in=DONORS_TO_RECIPIENTS[user_blood_type])
        .filter(hospital__in=CAZA_HOSPITALS[user_caza])
        .order_by("-date_added")
    )
    return render(request, "posts/post-grid.html", {"posts": posts})


def all_posts(request):
    posts = Post.objects.filter(fullfilled=False).order_by("-date_added")
    return render(request, "posts/post-grid.html", {"posts": posts})


@login_required(login_url="/users/login/")
def detailed_post(request, post_id):
    post = Post.objects.get(pk=post_id)
    location_data = HOSPITAL_LOCATION_DATA[post.hospital]
    can_recieve_from = ", ".join(DONORS_OF[post.blood_type])
    return render(
        request,
        "posts/detailed-post.html",
        {
            "post": post,
            "location_data": location_data,
            "can_recieve_from": can_recieve_from,
        },
    )


@login_required(login_url="/users/login/")
def my_posts(request):
    if request.method == "POST":
        # A user's own posts could be marked as fullfilled or marked as unfullfilled on the same page
        # Therefore we check which action the user wants to take based on the input name
        # which is stored in the post request
        if "mark_fullfilled_post_id" in request.POST:
            post_id = request.POST.get("mark_fullfilled_post_id")
            post = Post.objects.get(pk=post_id)
            post.fullfilled = True
            post.save()
        elif "mark_unfullfilled_post_id":
            post_id = request.POST.get("mark_unfullfilled_post_id")
            post = Post.objects.get(pk=post_id)
            post.fullfilled = False
            post.save()

        return redirect("posts:my-posts")
    else:
        posts = Post.objects.filter(user=request.user).order_by(
            "fullfilled",
            "-date_added",
        )
        return render(request, "posts/my-posts.html", {"posts": posts})


@login_required(login_url="/users/login/")
def whatsapp_group_link(request):
    if request.method == "GET":
        # TODO: make sure that https:// is included in the link
        # group_link = "https://www.youtube.com"
        group_link = getinvitelink()
        return redirect(group_link)


@login_required(login_url="/users/login/")
def add_post(request):
    if request.method == "POST":
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            hospital = form.cleaned_data["hospital"]
            post.caza = HOSPITAL_CAZAS[hospital]
            post.save()

            # TODO enable when notifications APIs are ready

            notify_compatible_users(
                post.blood_type,
                post.hospital,
                DONORS_OF[post.blood_type],
                post.caza,
            )

            msg = f"{post.blood_type} needed at {hospital} {post.description}"
            print(msg)
            send_whatsapp_message(message=msg)

            messages.success(request, "Post Added Successfully.")
            return redirect("posts:my-posts")
    else:
        form = PostForm()
    return render(request, "posts/add-post.html", {"form": form})
