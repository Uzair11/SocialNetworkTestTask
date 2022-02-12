from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from users.models import User, Post
from faker import Faker


class UserSignUpTestCase(APITestCase):

    def test_register_user(self):
        # Prepare data
        user = User.objects.create(
            username='testUser',
            first_name='test',
            last_name='test',
            email='testUser@gmail.com',
            password='TestUser1234'
        )
        self.assertIsInstance(user, User)
        self.assertEqual(user.email, 'testUser@gmail.com')

    def test_create_post(self):
        user = User.objects.create(
            username='testUser',
            first_name='test',
            last_name='test',
            email='testUser@gmail.com',
            password='TestUser1234'
        )
        post = Post.objects.create(
            title='testTitle',
            body='testBody',
            posted_by=user
        )
        self.assertIsInstance(post, Post)
        self.assertEqual(post.title, 'testTitle')
