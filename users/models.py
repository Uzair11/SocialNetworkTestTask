from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models


class User(AbstractUser):
    email = models.EmailField(_('email address'), unique=True)



class Post(models.Model):
    title = models.CharField(max_length=255)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_by')
    body = models.TextField()
    post_date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, through='PostLike')

    def __str__(self):
        return self.title + ' | ' + str(self.posted_by)


class PostLike(models.Model):
    user_who_liked = models.ForeignKey(User, on_delete=models.CASCADE)
    post_liked = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user_who_liked', 'post_liked',)