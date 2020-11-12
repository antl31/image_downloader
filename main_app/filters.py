import django_filters
from main_app.models import Image


class ImageFilter(django_filters.FilterSet):
    """
    filters for search endpoint by fields author,tags will find all case insensitive like words
    """
    author = django_filters.CharFilter(field_name="author", lookup_expr="icontains")
    tags = django_filters.CharFilter(field_name="tags", lookup_expr="icontains")

    class Meta:
        model = Image
        fields = ["author", "tags"]
