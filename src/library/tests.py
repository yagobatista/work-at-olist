
from datetime import datetime

from django.core.management import call_command
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from library.models import Author, Book
from library.factories import AuthorFactory, BookFactory


class BookTestsCreate(APITestCase):
    """
    Test bereaver of creating books
    """

    def setUp(self):
        AuthorFactory.create_batch(3)
        self.data = {
            'name': 'book test',
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
        Test missing name attribute
        """
        self._raise_error_on_attribute('name')

    def test_create_book_missing_attribute_edition(self):
        """
        Test missing edition attribute
        """
        self.data.pop('edition')
        response = self._create()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('edition'), 1)

    def test_create_book_missing_attribute_authors(self):
        """
        Test missing authors attribute
        """
        self._raise_error_on_attribute('authors')

    def test_create_book_missing_attribute_pubication_year(self):
        """
        Test missing publication_year attribute
        """
        self._raise_error_on_attribute('publication_year')

    def test_create_book_next_year(self):
        """
        Test creta book with publication year to the future
        """
        self.data.update({
            'publication_year': datetime.now().year + 1,
        })
        self._raise_error_on_attribute('publication_year')

    def test_create_book_one_author(self):
        """
        Test creta book with one author
        """
        self.data.update({
            'authors': Author.objects.first().pk,
        })
        response = self._create()
        authors = response.data.get('authors')
        self.assertEqual(len(authors), 1)

    def test_create_book_multiple_authors(self):
        """
        Test creta book with multiple author
        """
        response = self._create()
        authors = response.data.get('authors')
        self.assertEqual(len(authors), 3)


class BookTestsDelete(APITestCase):
    """
    Test delete book
    """

    def setUp(self):
        authors = AuthorFactory.create_batch(3)
        self.book = BookFactory(authors=authors)

    def test_delete_book(self):
        """
        Test deleting book
        """
        book_pk = self.book.pk
        url = '{}{}/'.format(reverse('book-list'), book_pk)
        self.client.delete(url)
        self.assertFalse(Book.objects.exists())


class BookTestsUpdate(APITestCase):
    """
    Test update Book
    """

    def setUp(self):
        authors = AuthorFactory.create_batch(3)
        self.book = BookFactory(authors=authors)
        self.data = {}

    def test_update_book(self):
        """
        Test update all attributes from book
        """
        book_pk = self.book.pk
        url = '{}{}/'.format(reverse('book-list'), book_pk)
        self.data.update({
            'name': 'update book test',
            'edition': 2,
            'publication_year': 2004,
            'authors': [Author.objects.first().pk],
        })
        put_response = self.client.put(url, self.data, format='json')
        put_response.data.pop('pk')
        self.assertEqual(self.data, put_response.data)

    def test_partial_update_book(self):
        """
        Test update only authors attributes from book
        """
        book_pk = self.book.pk
        url = '{}{}/'.format(reverse('book-list'), book_pk)
        self.data.update({
            'authors': [Author.objects.first().pk],
        })
        patch_response = self.client.patch(url, self.data, format='json')
        patch_response.data.pop('pk')
        self.assertEqual(self.data.get('authors'),
                         patch_response.data.get('authors'))


class BookTestsRetrieve(APITestCase):
    """
    Test retrieve Books
    """

    def _get(self, attribute_name, value):
        url = reverse('book-list')
        data = {}
        data[attribute_name] = value
        get_response = self.client.get(
            url,
            data=data,
            format='json',
        )
        return get_response.data.get('results')

    def test_retrieve_books_pagination(self):
        """
        Test items per page and count total
        """
        authors = AuthorFactory.create_batch(3)
        BookFactory.create_batch(50, authors=authors)

        url = reverse('book-list')
        get_response = self.client.get(url, format='json')
        count_total = get_response.data.get('count')

        self.assertEqual(count_total, 50)

    def test_retrieve_books_filter_name(self):
        """
        Test Filter books by name ya
        """
        authors = AuthorFactory.create_batch(3)
        BookFactory.create_batch(10, authors=authors)
        first_author = authors[0]

        BookFactory(name='tai ya', authors=[first_author])
        BookFactory(name='yaya', authors=[first_author])
        data = self._get('name', 'ya')

        self.assertEqual(len(data), 2)

    def test_retrieve_books_filter_publication_year(self):
        """
        Test Filter books published in 2019
        """
        authors = AuthorFactory.create_batch(3)
        first_author = authors[0]
        publication_year = 2019

        BookFactory.create_batch(10, authors=authors, publication_year=2000)
        BookFactory.create_batch(
            3,
            authors=[first_author],
            publication_year=publication_year,
        )

        data = self._get('publication_year', publication_year)
        first, second, third = data

        self.assertEqual(len(data), 3)
        self.assertEqual(first.get('publication_year'), publication_year)
        self.assertEqual(second.get('publication_year'), publication_year)
        self.assertEqual(third.get('publication_year'), publication_year)

    def test_retrieve_books_filter_edition(self):
        """
        Test Filter books by second edition
        """
        authors = AuthorFactory.create_batch(3)
        first_author = authors[0]
        edition = 2

        BookFactory.create_batch(10, authors=authors)
        BookFactory.create_batch(2, authors=[first_author], edition=edition)

        data = self._get('edition', edition)
        first, second = data

        self.assertEqual(len(data), 2)
        self.assertEqual(first.get('edition'), edition)
        self.assertEqual(second.get('edition'), edition)

    def test_retrieve_books_filter_author(self):
        """
        Test Filter books by author
        """
        authors = AuthorFactory.create_batch(3)
        first_author, second_author, third_author = authors
        author = third_author.pk

        BookFactory.create_batch(5, authors=[first_author])
        BookFactory.create_batch(10, authors=[second_author])
        BookFactory.create_batch(2, authors=[third_author])

        data = self._get('author', author)
        first, second = data

        self.assertEqual(len(data), 2)
        self.assertEqual(first.get('authors'), [author])
        self.assertEqual(second.get('authors'), [author])

    def test_retrieve_books_filter_co_author(self):
        """
        Test Filter books by auhtor and co-author
        """
        authors = AuthorFactory.create_batch(3)
        first_author, second_author, third_author = authors
        author = third_author.pk

        BookFactory.create_batch(1, authors=[first_author, author])
        BookFactory.create_batch(10, authors=[second_author])
        BookFactory.create_batch(2, authors=[author])

        data = self._get('author', author)
        first, second, third = data

        self.assertEqual(len(data), 3)
        self.assertIn(author, first.get('authors'), )
        self.assertIn(author, second.get('authors'))
        self.assertIn(author, third.get('authors'))


class AuthorTestImportCommand(TestCase):
    """
    Test Command that imports Authors data
    """

    def test_command(self):
        self.assertFalse(Author.objects.exists())
        call_command('import_authors', 'library/authors.csv')
        self.assertTrue(Author.objects.exists())


class AuthorTestCreate(APITestCase):
    """
    Test bereaver of creating Authors
    """

    def setUp(self):
        self.data = {
            'name': 'Author 1',
        }

    def test_create_author(self):
        """
        Test Authors name
        """
        url = reverse('author-list')
        post_response = self.client.post(url, self.data, format='json')
        data = post_response.data
        self.assertTrue(Author.objects.exists())
        self.assertEqual(data.get('name'), 'Author 1')


class AuthorTestUpdate(APITestCase):
    """
    Test bereaver of updating Authors
    """

    def test_updating_author_name(self):
        """
        Test update of Authors name
        """
        author = AuthorFactory()
        url = '{}{}/'.format(reverse('author-list'), author.pk)
        data = {
            'name': 'New Name',
        }
        post_response = self.client.put(url, data, format='json')
        data = post_response.data
        self.assertEqual(data.get('name'), 'New Name')


class AuthorTestDelete(APITestCase):
    """
    Test bereaver of deleting Authors
    """

    def test_delete(self):
        """
        Test delete Authors
        """
        author = AuthorFactory()
        url = '{}{}/'.format(reverse('author-list'), author.pk)
        self.client.delete(url, format='json')
        self.assertFalse(Author.objects.exists())


class AuthorTestRetrieve(APITestCase):
    """
    Test bereaver of retriving Authors
    """

    def test_retrieve_authors_pagination(self):
        """
        Test items per page and count total
        """
        AuthorFactory.create_batch(40)

        url = reverse('author-list')
        get_response = self.client.get(url, format='json')
        count_total = get_response.data.get('count')

        self.assertEqual(count_total, 40)

    def test_retrieve_authors_filter_name(self):
        AuthorFactory.create_batch(10)
        AuthorFactory(name='New Author 1')
        AuthorFactory(name='New Author 2')

        url = reverse('author-list')
        get_response = self.client.get(
            url,
            data={
                'name': 'New Author'
            },
            format='json',
        )
        data = get_response.data.get('results')
        self.assertEqual(len(data), 2)
