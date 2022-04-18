import scrapy

from ..items import NewsItem
from ..loaders import NewsLoader


class WSJSpider(scrapy.Spider):
    name = "wallstreetjournal"
    db_name = "The Wall Street Journal"
    start_urls = [
        "https://www.wsj.com/news/latest-headlines/",
    ]

    def parse(self, response, **kwargs):
        for article in response.css("main#main article"):
            relative_url = article.css("a::attr(href)").get()
            absolute_url = response.urljoin(relative_url)
            source_unique_id = article.css("a::attr(href)").re(r"-(\d*\?)")[0][1:-1]

            kws = {
                "title": article.css("a span::text").get(),
                "source_name": self.db_name,
                "source_unique_id": source_unique_id,
                "url": absolute_url,
                "img_url": article.css("img::attr(src)").get(),
                "description": None,
            }

            item = NewsLoader(item=NewsItem(**kws), response=response)

            yield item.load_item()
