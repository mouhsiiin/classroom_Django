from django.urls import path
from .views import (
    post_list_view, post_detail_view, post_edit_view, post_delete_view,
    add_like, add_dislike, add_comment_like, add_comment_dislike,
    comment_reply_view, editprofile, profile, picture_upload, add_comment, get_comments, search
)
from .chat import chat, create_conversation, send_message, get_messages

app_name = 'socialmedia'
urlpatterns = [
    path('', post_list_view, name='post-list'),
    path('post/<int:pk>/', post_detail_view, name='post-detail'),
    path('post/edit/<int:pk>/', post_edit_view, name='post-edit'),
    path('post/delete/<int:pk>/', post_delete_view, name='post-delete'),
    path('post/<int:pk>/like', add_like, name='like'),
    path('post/<int:pk>/dislike', add_dislike, name='dislike'),
    path('post/<int:post_pk>/comment/<int:pk>/like', add_comment_like, name='comment-like'),
    path('post/<int:post_pk>/comment/<int:pk>/dislike', add_comment_dislike, name='comment-dislike'),
    path('post/<int:post_pk>/comment/<int:pk>/reply', comment_reply_view, name='comment-reply'),
    path('post/<int:post_pk>/comments/', get_comments, name='get_comments'),
    path('editProfile', editprofile, name='editprofile'),
    path('profile/<str:username>/', profile, name='profile'),
    path('picture_upload', picture_upload, name='picture_upload'),
    path('chat/', chat, name='chat'),
    path('create_conversation/', create_conversation, name='create_conversation'),
    path('send_message/', send_message, name='send_message'),
    path('get_messages/', get_messages, name='get_messages'),
    path('search/', search, name='search'),


]

