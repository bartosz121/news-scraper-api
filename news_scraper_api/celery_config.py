import os
from news_scraper_api.config import get_config
from dotenv import load_dotenv

load_dotenv()
config = get_config()


timezone = "Europe/Warsaw"
broker_url = os.getenv("CELERY_BROKER_URL")
result_backend = config.MONGODB_SETTINGS["host"]
task_serializer = "json"
result_serializer = "json"
enable_utc = True
worker_max_tasks_per_child = 1  # for scrapy crawlers to work with celery tasks; see https://stackoverflow.com/a/22170168/17755169
