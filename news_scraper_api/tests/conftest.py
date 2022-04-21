import pytest
from mongoengine import connect, disconnect

from news_scraper_api import config
from news_scraper_api.app import create_app
from news_scraper_api.models.article import Article
from news_scraper_api.tests.mock_data import mock_articles


@pytest.fixture(scope="module")
def mock_ids():
    """
    Get mongo ids of added mock articles in `db`.

    Used in tests to check results
    """
    mock_ids = []
    for a in Article.objects():
        mock_ids.append(a["id"])

    return mock_ids


@pytest.fixture(scope="module")
def db():
    connect("mongomockdb", host="mongomock://localhost")
    for a in mock_articles:
        a = Article(**a).save()

    yield

    disconnect()


@pytest.fixture
def app(db):
    app = create_app(config.TestConfig())
    return app


@pytest.fixture
def client(app):
    return app.test_client()
