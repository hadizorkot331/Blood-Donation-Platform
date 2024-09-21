from django.urls import path
from . import views

app_name = "posts"

urlpatterns = [
    path("", views.home, name="home"),
    path("all-posts/", views.all_posts, name="all-posts"),
    path("whatsapp-group-link/", views.whatsapp_group_link, name="whatsapp-group-link"),  # type: ignore
    path("add-post/", views.add_post, name="add-post"),
    path("my-posts/", views.my_posts, name="my-posts"),
    path("detailed-post/<int:post_id>/", views.detailed_post, name="detailed-post"),
]
