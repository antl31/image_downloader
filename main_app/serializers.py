from urllib.request import urlopen
from tempfile import NamedTemporaryFile

from rest_framework import serializers
from django.core.files import File

from main_app.models import Image


class ImageSerializer(serializers.ModelSerializer):
    image_url = serializers.URLField()
    image_file = serializers.ImageField(required=False)

    class Meta:
        model = Image
        fields = ("external_id", "author", "tags", "image_file", "image_url")

    def create(self, validated_data):
        """
        override create instance method
        """
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(urlopen(validated_data["image_url"]).read())
        img_temp.name = f"{validated_data['external_id']}.jpg"

        instance = Image.objects.create(
            external_id=validated_data["external_id"],
            author=validated_data["author"],
            tags=validated_data["tags"],
            image_file=File(img_temp),
        )
        img_temp.flush()

        return instance

    def update(self, instance, validated_data):
        """
        override update instance method
        """
        img_temp = NamedTemporaryFile(delete=True)
        img_temp.write(urlopen(validated_data["image_url"]).read())
        img_temp.name = f"{validated_data['external_id']}.jpg"
        instance.external_id = validated_data["external_id"]
        instance.author = validated_data["author"]
        instance.image_file = File(img_temp)
        instance.save()

        img_temp.flush()

        return instance

    def get_photo_url(self, instance):
        """
        return url for download image
        """
        request = self.context.get("request")
        photo_url = instance.image_file.url
        return request.build_absolute_uri(photo_url)

    def to_representation(self, instance):
        """
        override response
        """
        return self.get_photo_url(instance)
