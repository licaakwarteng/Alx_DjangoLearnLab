from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post, Comment

class CommentTests(TestCase):
    def setUp(self):
        self.u1 = User.objects.create_user('u1', password='pass')
        self.u2 = User.objects.create_user('u2', password='pass')
        self.post = Post.objects.create(title='T', content='C', author=self.u1)

    def test_create_comment_requires_login(self):
        url = reverse('comment-create', kwargs={'post_pk': self.post.pk})
        resp = self.client.post(url, {'content': 'Hello'})
        # not logged in -> redirect to login
        self.assertEqual(resp.status_code, 302)
        self.client.login(username='u2', password='pass')
        resp2 = self.client.post(url, {'content': 'Hi!'})
        self.assertEqual(resp2.status_code, 302)
        self.assertTrue(Comment.objects.filter(post=self.post, author=self.u2, content='Hi!').exists())

    def test_only_author_can_edit_or_delete(self):
        comment = Comment.objects.create(post=self.post, author=self.u1, content='x')
        edit_url = reverse('comment-update', kwargs={'post_pk': self.post.pk, 'pk': comment.pk})
        delete_url = reverse('comment-delete', kwargs={'post_pk': self.post.pk, 'pk': comment.pk})

        self.client.login(username='u2', password='pass')
        r = self.client.get(edit_url)
        self.assertEqual(r.status_code, 403)  # UserPassesTestMixin defaults to 403

        r2 = self.client.post(delete_url)
        self.assertEqual(r2.status_code, 403)
