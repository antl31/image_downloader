import logging

from celery import shared_task

from main_app.service import ImageDownloader

logger = logging.getLogger(__name__)


@shared_task
def cron_update_images():
    logger.info("cron job update_images started")
    image_downloader = ImageDownloader()
    image_downloader.update_or_create_images()
    logger.info("cron job update_images finished")
