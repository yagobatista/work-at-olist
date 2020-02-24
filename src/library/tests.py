
from datetime import datetime

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from library.models import Author, Book


class BookTests(APITestCase):

    def setUp(self):
        authors = [Author(name='Author1'), Author(
            name='Author 2'), Author(name='Author 3')]
        Author.objects.bulk_create(authors)
        # first_author = Author.objects.first()
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
        Teste creta book with multiple author
        """
        response = self._create()
        book_pk = response.data.get('pk')
        url = reverse('book-list')
        import ipdb; ipdb.set_trace()
        self.client.delete()
        self.assertEqual(len(authors), 3)
