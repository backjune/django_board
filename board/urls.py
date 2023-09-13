from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

app_name = "board"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("user/register/", views.RegisterView.as_view(), name="register"),
    path("user/login/", views.CustomLoginView.as_view(), name="login"),
    path("user/logout/", auth_view.LogoutView.as_view(), name="logout"),
    path("user/update/", views.CustomUserUpdateView.as_view(), name="user_update"),
    path("user/update/profile_image/", views.CustomUserUpdateProfileImgView.as_view(),
         name="user_update_profile_image"),
    path("user/delete/profile_image/", views.DeleteProfileImgView.as_view(), name="user_profile_image_delete"),

    path("post/create/", views.PostCreateView.as_view(), name="post_create"),
    path("post/<int:pk>/", views.PostDetailView.as_view(), name="post_detail"),
    path("post/update/<int:pk>/", views.PostUpdateView.as_view(), name="post_update"),
    path("post/delete/<int:pk>/", views.PostDeleteView.as_view(), name="post_delete"),
    path("post/like/<int:pk>/", views.PostLikeView.as_view(), name="post_like"),

    path("comment/create/<int:board_id>/", views.CommentCreateView.as_view(), name="comment_create"),
    path("comment/delete/<int:pk>/", views.CommentDeleteView.as_view(), name="comment_delete"),
]
