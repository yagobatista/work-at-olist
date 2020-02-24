from rest_framework.viewsets import ModelViewSet
from library.models import Author
from library.serializers import AuthorSerializer


class AuthorViewSet(ModelViewSet):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()
