
from django.db import models
from django.conf import settings
from django.utils import timezone



class Post(models.Model):
    body = models.TextField()
    image = models.ImageField(upload_to='uploads/post_photos', blank=True, null=True)
    video = models.FileField(upload_to='uploads/post_videos', blank=True, null=True)
   
    created_on = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(settings.AUTH_USER_MODEL , on_delete=models.CASCADE)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='likes')
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='dislikes')


class Comment(models.Model):
    comment = models.TextField()
    created_on = models.DateTimeField(default=timezone.now)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='comment_likes')
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL , blank=True, related_name='comment_dislikes')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='+')
    @property
    def children(self):
        return Comment.objects.filter(parent=self).order_by('-created_on').all()
    @property
    def is_parent(self):
     if self.parent is None:
        return True
    
     return False    