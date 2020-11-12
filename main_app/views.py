from django_filters import rest_framework as filters
from rest_framework import mixins
from rest_framework import viewsets

from main_app.models import Image
from main_app.serializers import ImageSerializer
from main_app.filters import ImageFilter


class ImageSearchViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ImageFilter
