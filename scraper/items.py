import scrapy
from .loaders import NewsLoader


class NewsItem(scrapy.Item):
    title = scrapy.Field(serializer=str)
    source_name = scrapy.Field(serializer=str)
    source_unique_id = scrapy.Field(serializer=str)
    url = scrapy.Field(serializer=str)
    img_url = scrapy.Field(serializer=str)
    description = scrapy.Field(serializer=str)
