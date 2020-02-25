from library.models import Author, Book
from django_filters import CharFilter, BaseInFilter, FilterSet


class AuthorFilterSet(FilterSet):
    name = CharFilter(lookup_expr='contains')

    class Meta:
        model = Author
        fields = ['name']


class BookFilterSet(FilterSet):
    name = CharFilter(lookup_expr='contains')
    author = BaseInFilter('authors')

    class Meta:
        model = Book
        fields = [
            'name',
            'publication_year',
            'edition',
            'author',
        ]
