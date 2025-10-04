from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Post, Comment, Tag

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


class TagSearchTests(TestCase):
    def setUp(self):
        u = User.objects.create_user('u', password='p')
        self.p1 = Post.objects.create(title='Django tips', content='Some content about Django', author=u)
        self.p2 = Post.objects.create(title='Python notes', content='Python content', author=u)
        # create tag and attach
        tag = Tag.objects.create(name='django')
        self.p1.tags.add(tag)

    def test_tag_list_view(self):
        resp = self.client.get(reverse('posts-by-tag', kwargs={'tag_name': 'django'}))
        self.assertContains(resp, 'Django tips')
        self.assertNotContains(resp, 'Python notes')

    def test_search_by_keyword(self):
        resp = self.client.get(reverse('search') + '?q=Python')
        self.assertContains(resp, 'Python notes')
        self.assertNotContains(resp, 'Django tips')

    def test_search_by_tag(self):
        resp = self.client.get(reverse('search') + '?q=django')
        self.assertContains(resp, 'Django tips')