import os
import logging

import requests
from rest_framework import status

from main_app.models import Image
from main_app.serializers import ImageSerializer

logger = logging.getLogger(__name__)

AUTH_URL = os.getenv("AUTH_URL")
IMAGE_URL = os.getenv("IMAGE_URL")
API_KEY = os.getenv("API_KEY")


class ImageDownloader:
    def __init__(
        self, default_auth_url=AUTH_URL, default_image_url=IMAGE_URL, apikey=API_KEY
    ):
        self.auth = False
        self.token = ""
        if (default_auth_url is None) or (default_image_url is None) or (apikey is None):
            raise ValueError("urls or apikey cant be empty!")

        self.auth_url = default_auth_url
        self.image_url = default_image_url
        self.apikey = apikey
        self.auth_in_external_api()

    def auth_in_external_api(self):
        """
        method to authenticate on external api by apikey
        """
        body = {"apiKey": self.apikey}
        try:
            r = requests.post(self.auth_url, json=body)
            if r.status_code == status.HTTP_200_OK:
                response = r.json()
                self.auth = response.get("auth")
                self.token = response.get("token")
                logger.info("Authenticate was success")
            else:
                logger.error("auth endpoint get error status code")
        except Exception as e:
            logger.error(f"auth not corrected {e}")

    def get_image_response_by_url(self, url):
        """
        get response by url and using auth credentials
        """
        response = {}
        if url:
            if self.auth:
                headers = {"Authorization": f"Bearer {self.token}"}
                try:
                    r = requests.get(url, headers=headers)
                    if r.status_code == status.HTTP_200_OK:
                        response = r.json()
                    elif r.status_code == status.HTTP_401_UNAUTHORIZED:
                        self.auth_in_external_api()
                        if self.auth:
                            headers = {"Authorization": f"Bearer {self.token}"}
                            r = requests.get(url, headers=headers)
                            if r.status_code == status.HTTP_200_OK:
                                response = r.json()
                except Exception as e:
                    logger.error(f"Something wrong {e}")
        return response

    def get_all_images(self):
        """
        get all images ids from image url
        """
        init_response = self.get_image_response_by_url(self.image_url)
        image_ids = [i.get("id") for i in init_response.get("pictures")]
        max_pages = init_response.get("pageCount") + 1
        for page_number in range(2, max_pages):
            next_page_url = f"{self.image_url}?page={page_number}"
            image_ids.extend(
                [
                    i.get("id")
                    for i in self.get_image_response_by_url(next_page_url).get(
                        "pictures"
                    )
                ]
            )
        logger.info(f"Get all images successful")
        return image_ids

    def update_or_create_images(self):
        """
        update or create new image records in table Image
        """
        image_ids = self.get_all_images()
        for image_id in image_ids:
            get_image_url = f"{self.image_url}{image_id}"
            response = self.get_image_response_by_url(get_image_url)
            cropped_image_url = response.get("cropped_picture").replace(
                " ", "%20"
            )  # fix invalid symbols in url
            data = {
                "author": response.get("author"),
                "external_id": response.get("id"),
                "tags": response.get("tags"),
                "image_url": cropped_image_url,
            }
            try:
                instance = Image.objects.get(external_id=response.get("id"))
                image = ImageSerializer(instance, data=data)
                if image.is_valid():
                    image.save()
                else:
                    logger.error(image.errors)
            except Image.DoesNotExist:
                image = ImageSerializer(data=data)
                if image.is_valid():
                    image.save()
        logger.info(f"Image table was successful updated/created")
