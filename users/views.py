from django.contrib.auth import get_user_model
from django.shortcuts import render

# Create your views here.
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from users.serializers import UserSerializer, UserRegisterSerializer, PostSerializer, PostLikeSerializer, UserPostSerializer
from django.contrib.auth import login, logout, authenticate
from rest_framework import exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenViewBase
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from users.models import Post, PostLike
from users.permissions import AccessPermission
import operator
import json
from django.db.models import Count
from rest_framework.renderers import JSONRenderer


UserModel = get_user_model()

class TokenObtainUserSerializer(TokenObtainPairSerializer):

    def get_token(self, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['username'] = user.username
        return token

    def validate(self, attrs):
        try:
            data = super().validate(attrs)
        except Exception as e:
            raise exceptions.ParseError(
                {"detail": "Username or Password is Incorrect!"}
            )
        data["token"] = {"access": data["access"], "refresh": data["refresh"]}
        del data["access"]
        del data["refresh"]
        data["user"] = UserSerializer(self.user).data
        return data


class TokenObtainUserView(TokenViewBase):

    serializer_class = TokenObtainUserSerializer



class UserModelViewSet(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer


class UserRegisterViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        method="post",
        request_body=UserRegisterSerializer(),
    )
    @action(detail=False, methods=["post"], )
    def register_user(self, request):
        """Register User"""
        ser = UserRegisterSerializer(data=request.data)
        ser.is_valid(raise_exception=True)

        user = UserModel.objects.create(
            first_name=ser.validated_data['first_name'],
            last_name=ser.validated_data['last_name'],
            email=ser.validated_data['email'],
            username=ser.validated_data['username'],
        )
        user.set_password(ser.validated_data['password'])
        user.save()

        return Response(status=200, data=UserSerializer(user).data)


    @swagger_auto_schema(
        method="get",
    )
    @action(detail=False, methods=["get"], )
    def get_user_profile(self, request):
        return Response(status=200, data=UserSerializer(request.user).data)


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated, AccessPermission)
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class PostView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        post_id = kwargs.get('id')
        if post_id:
            try:
                post = Post.objects.get(id=post_id)
                return Response(PostSerializer(post).data, status=status.HTTP_200_OK)
            except ObjectDoesNotExist:
                return Response({'error': "No post found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            posts = Post.objects.all()
            posts_data = PostSerializer(posts, many=True).data
            return Response(data=posts_data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(posted_by=request.user, title=serializer.validated_data['title'], body=serializer.validated_data['body'])
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        post_id = kwargs.get('id')
        try:
            post = Post.objects.get(id=post_id)
            if post.posted_by.id == request.user.id:
                post.delete()
                return Response({'msg': 'Post deleted'}, status=status.HTTP_200_OK)
            else:
                return Response({'Error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        except ObjectDoesNotExist:
            return Response({'error': "No post found"}, status=status.HTTP_404_NOT_FOUND)
        



class LikesPostViewSet(viewsets.ViewSet):
    @swagger_auto_schema(
        method="post",
        request_body=PostLikeSerializer(),
    )
    @action(detail=False, methods=["post"], )
    def like_post(self, request):
        serializer = PostLikeSerializer(data=request.data)
        if serializer.is_valid():
            if Post.objects.filter(id=serializer.validated_data['post_liked'].id, posted_by=request.user).exists():
                return Response(data='You cannot like your own post', status=status.HTTP_400_BAD_REQUEST)
            if PostLike.objects.filter(user_who_liked=request.user, post_liked=serializer.validated_data['post_liked']).exists():
                return Response(data='Already Liked', status=status.HTTP_400_BAD_REQUEST)
            else:
                PostLike.objects.create(user_who_liked=request.user, post_liked=serializer.validated_data['post_liked'])
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        method="delete",
        request_body=PostLikeSerializer(),
    )
    @action(detail=False, methods=["delete"], )
    def unlike_post(self, request):
        serializer = PostLikeSerializer(data=request.data)
        if serializer.is_valid():
            if PostLike.objects.filter(user_who_liked=request.user, post_liked=serializer.validated_data['post_liked']).exists():
                PostLike.objects.filter(user_who_liked=request.user, post_liked=serializer.validated_data['post_liked']).delete()
                return Response(data='Like Removed', status=204)
            else:
                return Response(data='Like not exists', status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        method="get",
    )
    @action(detail=False, methods=["get"], )
    def user_posts(self, request):
        queryset = UserModel.objects.all().annotate(num_of_posts=Count('post_by')).order_by('-num_of_posts').values('id', 'email', 'first_name', 'last_name', 'username', 'num_of_posts')
        context = UserPostSerializer(queryset, many=True)
        print(context.data)
        return Response(data=context.data, status=status.HTTP_200_OK)