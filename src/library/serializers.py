from library.models import Author, Book
from rest_framework.serializers import ModelSerializer


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = ['pk', 'name']

class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
        fields = ['pk', 'name', 'edition', 'publication_year', 'authors', ]