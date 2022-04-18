import os
import httpx
from itemadapter import ItemAdapter
from .items import NewsItem
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
PIPELINE_BASE_URL = os.getenv("PIPELINE_BASE_URL")


class NewsPipeline:
    collection_name = "news"

    def open_spider(self, spider):
        self.client = httpx.Client()

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item: NewsItem, spider):
        r = self.client.post(
            f"{PIPELINE_BASE_URL}/api/v1/news?api_key={API_KEY}",
            json=ItemAdapter(item).asdict(),
        )
        return item
