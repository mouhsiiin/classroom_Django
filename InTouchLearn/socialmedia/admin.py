from django.contrib import admin
from .models import Post, Comment, message, conversation


admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(message)
admin.site.register(conversation)
