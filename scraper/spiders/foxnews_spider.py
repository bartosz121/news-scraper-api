import scrapy

from ..items import NewsItem
from ..loaders import NewsLoader


class FoxNewsSpider(scrapy.Spider):
    name = "foxnews"
    db_name = "Fox News"
    start_urls = [
        "https://www.foxnews.com/world/",
    ]

    def parse(self, response, **kwargs):
        for article in response.css("div.content.article-list article"):
            relative_url = article.css("div.info header h4.title a::attr(href)").get()
            absolute_url = response.urljoin(relative_url)

            kws = {
                "title": article.css("div.info header h4.title a::text").get(),
                "source_name": self.db_name,
                "source_unique_id": relative_url.split("/")[-1],
                "url": absolute_url,
                "img_url": article.css("div.m a img::attr(src)").get(),
                "description": article.css("div.info div.content p a::text").get(),
            }

            item = NewsLoader(item=NewsItem(**kws), response=response)

            yield item.load_item()
