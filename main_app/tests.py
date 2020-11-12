from rest_framework.test import APITestCase
from django.core.management import call_command
from main_app.service import ImageDownloader
from main_app.models import Image


class SearchEndpointTests(APITestCase):
    """
    Test for validate search query_params_of_search_endpoint
    """
    def setUp(self):
        call_command("loaddata", "main_app/fixtures/initial_data.json", verbosity=0)

    def test_get_images_by_search(self):
        response = self.client.get("/search/", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 20)

        response = self.client.get("/search/?tags=photography", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 7)

        response = self.client.get("/search/?tags=#photo&author=sea", format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)


class ImageDownloaderAuthTests(APITestCase):
    """
    Test for auth on external resource
    """
    def setUp(self):
        self.image_downloader = ImageDownloader()

    def test_validate_auth(self):
        self.assertTrue(self.image_downloader.auth)
        self.assertEqual(len(self.image_downloader.token), 40)


class ImageDownloaderUpdateImagesTests(APITestCase):
    """
    Test for validate updating of Image model by upload new records from external API
    """
    def setUp(self):
        call_command("loaddata", "main_app/fixtures/initial_data.json", verbosity=0)
        self.image_downloader = ImageDownloader()

    def test_get_update_images(self):
        self.assertEqual(Image.objects.count(), 20)
        self.image_downloader.update_or_create_images()
        self.assertEqual(Image.objects.count(), 259)


class ImageDownloaderCreateImagesTest(APITestCase):
    """
    Test for validate creating records in Image model by upload images from external API
    """
    def setUp(self):
        self.image_downloader = ImageDownloader()

    def test_get_update_images(self):
        self.assertEqual(Image.objects.count(), 0)
        self.image_downloader.update_or_create_images()
        self.assertEqual(Image.objects.count(), 259)
