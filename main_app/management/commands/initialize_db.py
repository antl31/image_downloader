import logging

from django.core.management.base import BaseCommand

from main_app.service import ImageDownloader

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Initialize db of images"

    def handle(self, *args, **options):
        logger.info("Started initialize db command")
        img_downloader = ImageDownloader()
        img_downloader.update_or_create_images()
        logger.info("Finished initialize db command")
