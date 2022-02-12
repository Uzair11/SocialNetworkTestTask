from django.contrib.auth import get_user_model
from rest_framework import serializers
from users.models import Post, PostLike
from django.db.models import Count
UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ['id', 'email', 'first_name', 'last_name', 'username', ]


class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        fields = ['id', 'email', 'first_name', 'last_name', 'username', 'password']


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id','title','body', 'posted_by','likes']
        read_only_fields = ('post_date',)

    def create(self, validated_data):
        try:
            validated_data.pop['posted_by']
        except Exception as e:
            pass
        instance = super(PostSerializer, self).create(validated_data)
        instance.posted_by = self.context['request'].user
        instance.save()
        return instance


class PostLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostLike
        fields = ('post_liked',)


class UserPostSerializer(serializers.ModelSerializer):
    num_of_posts = serializers.IntegerField(read_only=True)
    class Meta:
        model = UserModel
        fields = ['id', 'email', 'first_name', 'last_name', 'username', 'num_of_posts']
