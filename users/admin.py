from django.contrib import admin
from django.contrib.auth import get_user_model
from users.models import Post, PostLike

UserModel = get_user_model()

admin.site.register(UserModel)
admin.site.register(Post)
admin.site.register(PostLike)