from dotenv import load_dotenv
from celery import Celery
from celery.schedules import crontab
from twisted.internet import reactor
from scrapy import Spider
from scrapy.crawler import CrawlerRunner
from scrapy.utils.project import get_project_settings

from news_scraper_api import celery_config
from news_scraper_api.config import get_config

from scraper.spiders import (
    bbc_spider,
    cnn_spider,
    foxnews_spider,
    newyorktimes_spider,
    theeconomist_spider,
    thewashingtonpost_spider,
    wallstreetjournal_spider,
)


load_dotenv()


config = get_config()
celery = Celery(__name__)
celery.config_from_object(celery_config)

celery.conf.beat_schedule = {
    "crawl-news-every-three-hours": {
        "task": "news_scraper_api.core.tasks.crawl_all",
        "schedule": crontab(minute=0, hour="*/3"),
    },
}


def run_spider(spider: Spider):
    scrapy_settings = get_project_settings()
    runner = CrawlerRunner(settings=scrapy_settings)
    d = runner.crawl(spider)
    d.addBoth(lambda _: reactor.stop())
    reactor.run()  # the script will block here until the crawling is finished


@celery.task
def crawl_all():
    crawl_bbc.apply_async()
    crawl_cnn.apply_async()
    crawl_foxnews.apply_async()
    crawl_newyorktimes.apply_async()
    crawl_theeconomist.apply_async()
    crawl_thewashingtonpost.apply_async()
    crawl_wallstreetjournal.apply_async()


@celery.task
def crawl_bbc():
    run_spider(bbc_spider.BBCSpider)


@celery.task
def crawl_cnn():
    run_spider(cnn_spider.CNNSpider)


@celery.task
def crawl_foxnews():
    run_spider(foxnews_spider.FoxNewsSpider)


@celery.task
def crawl_newyorktimes():
    run_spider(newyorktimes_spider.NewYorkTimesSpider)


@celery.task
def crawl_theeconomist():
    run_spider(theeconomist_spider.TheEconomistSpider)


@celery.task
def crawl_thewashingtonpost():
    run_spider(thewashingtonpost_spider.TWPSpider)


@celery.task
def crawl_wallstreetjournal():
    run_spider(wallstreetjournal_spider.WSJSpider)
