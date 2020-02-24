
from datetime import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from library.models import Author, Book
from library.factories import AuthorFactory, BookFactory


class BookTests(APITestCase):

    def setUp(self):
        AuthorFactory.create_batch(3)
        self.data = {
            'name': 'book teste',
            'edition': 1,
            'publication_year': 2002,
            'authors': Author.objects.values_list('pk', flat=True),
        }

    def _create(self):
        url = reverse('book-list')
        return self.client.post(url, self.data, format='json')

    def _raise_error_on_attribute(self, attribute):
        self.data.pop(attribute)
        response = self._create()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(response.data.get(attribute, None))

    def test_create_book_missing_attribute_name(self):
        """
        Teste missing name attribute
        """
        self._raise_error_on_attribute('name')

    def test_create_book_missing_attribute_edition(self):
        """
        Teste missing edition attribute
        """
        self.data.pop('edition')
        response = self._create()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('edition'), 1)

    def test_create_book_missing_attribute_authors(self):
        """
        Teste missing authors attribute
        """
        self._raise_error_on_attribute('authors')

    def test_create_book_missing_attribute_pubication_year(self):
        """
        Teste missing publication_year attribute
        """
        self._raise_error_on_attribute('publication_year')

    def test_create_book_next_year(self):
        """
        Teste creta book with publication year to the future
        """
        self.data.update({
            'publication_year': datetime.now().year + 1,
        })
        self._raise_error_on_attribute('publication_year')

    def test_create_book_one_author(self):
        """
        Teste creta book with one author
        """
        self.data.update({
            'authors': Author.objects.first().pk,
        })
        response = self._create()
        authors = response.data.get('authors')
        self.assertEqual(len(authors), 1)

    def test_create_book_multiple_authors(self):
        """
        Teste creta book with multiple author
        """
        response = self._create()
        authors = response.data.get('authors')
        self.assertEqual(len(authors), 3)

    def test_delete_book(self):
        """
        Teste deleting book
        """
        response = self._create()
        self.assertTrue(Book.objects.exists())
        book_pk = response.data.get('pk')
        url = '{}{}/'.format(reverse('book-list'), book_pk)
        self.client.delete(url)
        self.assertFalse(Book.objects.exists())

    def test_update_book(self):
        """
        Teste update all attributes from book
        """
        response = self._create()
        book_pk = response.data.get('pk')
        url = '{}{}/'.format(reverse('book-list'), book_pk)
        self.data.update({
            'name': 'update book teste',
            'edition': 2,
            'publication_year': 2004,
            'authors': [Author.objects.first().pk],
        })
        put_response = self.client.put(url, self.data, format='json')
        put_response.data.pop('pk')
        self.assertEqual(self.data, put_response.data)

    def test_partial_update_book(self):
        """
        Teste update only authors attributes from book
        """
        response = self._create()
        book_pk = response.data.get('pk')
        url = '{}{}/'.format(reverse('book-list'), book_pk)
        self.data.update({
            'authors': [Author.objects.first().pk],
        })
        patch_response = self.client.patch(url, self.data, format='json')
        patch_response.data.pop('pk')
        self.assertEqual(self.data, patch_response.data)


class BookTestsRetrieve(APITestCase):
    """
    Teste retrieve Book
    """

    def test_retrieve_books_pagination(self):
        """
        Teste retrieve items per page and count total
        """
        BookFactory.create_batch(50)
        url = reverse('book-list')
        get_response = self.client.get(url, format='json')
        data = get_response.data.get('results')
        count_total = get_response.data.get('count')
        self.assertEqual(len(data), 10)
        self.assertEqual(count_total, 50)

    def test_retrieve_books_filter(self):
        """
        Teste retrieve Filter
        """
        authors = AuthorFactory.create_batch(3)
        BookFactory.create_batch(10, authors=authors)
        # book = BookFactory(authors=authors)
        url = reverse('book-list')
        authors = Book.objects.values_list('authors').order_by('authors')
        get_response = self.client.get(
            url,
            # data={
            #     ''
            # },
            format='json',
        )
        data = get_response.data.get('results')
        count_total = get_response.data.get('count')
        self.assertEqual(len(data), 10)
        self.assertEqual(count_total, 50)
