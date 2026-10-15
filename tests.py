from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .models import Post


class PostModelTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='author', password='pass1234'
        )

    def test_slug_is_generated(self):
        post = Post.objects.create(author=self.user, title='My Test Post', content='Body')
        self.assertTrue(post.slug)


class PostPermissionTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.author = User.objects.create_user(username='author', password='pass1234')
        self.other = User.objects.create_user(username='other', password='pass1234')
        self.post = Post.objects.create(author=self.author, title='Secret', content='Body')

    def test_author_can_edit(self):
        client = Client()
        client.login(username='author', password='pass1234')
        url = reverse('posts:post_edit', kwargs={'slug': self.post.slug})
        response = client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_other_cannot_edit(self):
        client = Client()
        client.login(username='other', password='pass1234')
        url = reverse('posts:post_edit', kwargs={'slug': self.post.slug})
        response = client.get(url)
        self.assertEqual(response.status_code, 403)
