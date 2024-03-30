from django.urls import path
from .views import (
    post_list_view, post_detail_view, post_edit_view, post_delete_view,
    add_like, add_dislike, add_comment_like, add_comment_dislike,
    comment_reply_view, editprofile, profile,
)

app_name = 'socialmedia'
urlpatterns = [
    path('', post_list_view, name='post-list'),
    path('post/<int:pk>/', post_detail_view, name='post-detail'),
    path('post/edit/<int:pk>/', post_edit_view, name='post-edit'),
    path('post/delete/<int:pk>/', post_delete_view, name='post-delete'),
    path('post/<int:pk>/like/', add_like, name='like'),
    path('post/<int:pk>/dislike/', add_dislike, name='dislike'),
    path('post/<int:post_pk>/comment/<int:pk>/like/', add_comment_like, name='comment-like'),
    path('post/<int:post_pk>/comment/<int:pk>/dislike/', add_comment_dislike, name='comment-dislike'),
    path('post/<int:post_pk>/comment/<int:pk>/reply/', comment_reply_view, name='comment-reply'),
    path('editProfile/', editprofile, name='editprofile'),
    path('profile/<str:username>/', profile, name='profile'),
  
]

