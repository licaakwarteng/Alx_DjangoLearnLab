from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Author, Book


class BookAPITestCase(APITestCase):
    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()

        # Create authors and books
        self.author = Author.objects.create(name='J.R.R. Tolkien')
        self.book1 = Book.objects.create(title='The Hobbit', publication_year=1937, author=self.author)
        self.book2 = Book.objects.create(title='The Lord of the Rings', publication_year=1954, author=self.author)

        self.list_url = reverse('book-list')
        self.create_url = reverse('book-create')
        self.update_url = reverse('book-update', args=[self.book1.pk])
        self.delete_url = reverse('book-delete', args=[self.book1.pk])
        self.detail_url = reverse('book-detail', args=[self.book1.pk])

    def test_list_books(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_book(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'The Hobbit')

    def test_create_book_requires_auth(self):
        data = {
            'title': 'Silmarillion',
            'publication_year': 1977,
            'author': self.author.id
        }
        # Without login
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # With login
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(self.create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_update_book(self):
        self.client.login(username='testuser', password='testpass')
        data = {
            'title': 'The Hobbit: Revised',
            'publication_year': 1937,
            'author': self.author.id
        }
        response = self.client.put(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'The Hobbit: Revised')

    def test_delete_book(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_filter_books_by_author(self):
        response = self.client.get(f"{self.list_url}?author={self.author.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_search_books_by_title(self):
        response = self.client.get(f"{self.list_url}?search=Hobbit")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'The Hobbit')

    def test_order_books_by_publication_year(self):
        response = self.client.get(f"{self.list_url}?ordering=publication_year")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['title'], 'The Hobbit')

        response = self.client.get(f"{self.list_url}?ordering=-publication_year")
        self.assertEqual(response.data[0]['title'], 'The Lord of the Rings')
