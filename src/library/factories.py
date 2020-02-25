from datetime import datetime

import factory
from factory import Sequence, SubFactory, RelatedFactory
from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyInteger

from library.models import Author, Book


class AuthorFactory(DjangoModelFactory):
    name = Sequence(lambda n: 'Author Name {0}'.format(n))

    class Meta:
        model = Author


class BookFactory(DjangoModelFactory):
    name = Sequence(lambda n: 'Book Name {0}'.format(n))
    publication_year = FuzzyInteger(-6000, datetime.now().year)

    @factory.post_generation
    def authors(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        for author in extracted:
            self.authors.add(author)

    class Meta:
        model = Book
