from rest_framework.viewsets import ModelViewSet
from library.models import Author, Book
from library.serializers import AuthorSerializer, BookSerializer
from library.filters import AuthorFilterSet, BookFilterSet


class AuthorViewSet(ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
    filterset_class = AuthorFilterSet


class BookViewSet(ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()
    filterset_class = BookFilterSet
