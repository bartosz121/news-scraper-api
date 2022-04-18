from itemloaders.processors import TakeFirst
from scrapy.loader import ItemLoader


class NewsLoader(ItemLoader):
    default_output_processor = TakeFirst()
