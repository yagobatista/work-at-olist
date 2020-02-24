from library.models import Author
from django_filters import CharFilter, FilterSet


class AuthorFilterSet(FilterSet):
    name = CharFilter(lookup_expr='contains')

    class Meta:
        model = Author
        fields = ['name']
