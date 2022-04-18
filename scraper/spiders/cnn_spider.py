import scrapy


class CNNSpider(scrapy.Spider):
    name = "cnn"
    db_name = "CNN"
    start_urls = [
        "https://edition.cnn.com/world/",
    ]

    def parse(self, response, **kwargs):
        for article in response.css("div.cd__wrapper"):
            relative_url = article.css("h3.cd__headline a::attr(href)").get()
            absolute_url = response.urljoin(relative_url)

            img_url = article.css("div.media img::attr(data-src-xsmall)").get()
            if img_url:
                img_url: str = img_url.lstrip("//")

            # There are many articles from other sources (not cnn) we dont want those
            if not absolute_url.startswith("https://edition.cnn.com"):
                continue

            yield {
                "title": article.css("span.cd__headline-text::text").get(),
                "source_name": self.db_name,
                "source_unique_id": relative_url.split("/")[-2],
                "url": absolute_url,
                "img_url": img_url,
                "description": None,
            }
