import os
from dotenv import load_dotenv
import pytest
from datetime import datetime, timezone
from mongoengine import connect, disconnect
from werkzeug.exceptions import HTTPException

from news_scraper_api import config
from news_scraper_api.app import create_app
from news_scraper_api.core.utils import get_object_or_404
from news_scraper_api.models.article import Article

load_dotenv()

API_KEY = os.getenv("API_KEY")

mock_articles = [
    {
        "title": "Title 1",
        "source_name": "BBC",
        "source_unique_id": "id1",
        "url": "url1",
        "img_url": "img_url1",
        "description": "description1",
        "created": datetime.fromtimestamp(1760896328, tz=timezone.utc),
    },
    {
        "title": "Title 2",
        "source_name": "CNN",
        "source_unique_id": "id2",
        "url": "url2",
        "img_url": "img_url2",
        "description": "description2",
        "created": datetime.fromtimestamp(1456393995, tz=timezone.utc),
    },
    {
        "title": "Title 3",
        "source_name": "BBC",
        "source_unique_id": "id3",
        "url": "url3",
        "img_url": "img_url3",
        "description": "description3",
        "created": datetime.fromtimestamp(1313621794, tz=timezone.utc),
    },
    {
        "title": "Title 4",
        "source_name": "Fox News",
        "source_unique_id": "id4",
        "url": "url4",
        "img_url": "img_url4",
        "description": "description4",
        "created": datetime.fromtimestamp(1129174872, tz=timezone.utc),
    },
]

mock_ids = []

post_request_data = {
    "title": "Title 5",
    "source_name": "BBC",
    "source_unique_id": "id5",
    "url": "url5",
    "img_url": "img_url5",
    "description": "description5",
}


@pytest.fixture(scope="module")
def db():
    connect("mongomockdb", host="mongomock://localhost")
    for a in mock_articles:
        a = Article(**a).save()
        mock_ids.append(a.id)
        print(a.id)

    yield

    disconnect()


@pytest.fixture
def app(db):
    app = create_app(config.TestConfig())
    return app


@pytest.fixture
def client(app):
    return app.test_client()


def test_get_object_or_404(app):
    with pytest.raises(HTTPException):
        get_object_or_404(Article, source_unique_id="id657569213")


# Tests for "/api/v1/news/"


def test_get_article(client):
    expected_length = len(mock_articles)
    with client:
        r = client.get("/api/v1/news")
        assert r.status_code == 200

        data = r.get_json()

        assert len(data) == expected_length

        # Remember that this endpoint sorts articles by `-created`
        assert all(
            [
                str(expected_id) == article["id"]
                for expected_id, article in zip(mock_ids, data)
            ]
        )


def test_get_article_by_id(client):
    """Tests /api/v1/news/`id`"""
    mock_article_index = 2

    with client:
        r = client.get(f"/api/v1/news/{mock_ids[mock_article_index]}")
        assert r.status_code == 200

        data = r.get_json()
        assert data["id"] == str(mock_ids[mock_article_index])
        assert data["title"] == mock_articles[mock_article_index]["title"]


def test_get_article_by_source_name(client):
    source_name = "BBC"
    expected_length = len([a for a in mock_articles if a["source_name"] == source_name])

    with client:
        r = client.get(f"/api/v1/news?source={source_name}")
        assert r.status_code == 200

        data = r.get_json()
        assert len(data) == expected_length


# Test `api_key_required decorator`- POST


def test_no_api_key_provided(client):
    with client:
        r = client.post("/api/v1/news", data=post_request_data)

        assert r.status_code == 401
        data = r.get_json()

        assert data["message"] == "Please provide an API Key"


def test_api_key_not_valid(client):
    with client:
        r = client.post(
            "/api/v1/news?api_key=not-valid-api-key", data=post_request_data
        )

    assert r.status_code == 401
    data = r.get_json()

    assert data["message"] == "API Key not valid"


# Tests for POST, PUT, DELETE


def test_news_post_request(client):
    with client:
        r = client.post(f"/api/v1/news?api_key={API_KEY}", json=post_request_data)

        assert r.status_code == 201

        data = r.get_json()

        assert data["title"] == post_request_data["title"]


def test_news_put_request(client):
    mock_article_id = mock_ids[0]
    updated_title = "Updated title"

    with client:
        r1 = client.get(f"/api/v1/news/{mock_article_id}")
        assert r1.status_code == 200

        put_request_data = r1.get_json()
        put_request_data["title"] = updated_title
        put_request_data.pop("id")
        put_request_data.pop("created")

        r2 = client.put(
            f"/api/v1/news/{mock_article_id}?api_key={API_KEY}",
            json=put_request_data,
        )
        assert r2.status_code == 200

        data = r2.get_json()

        assert data["id"] == str(mock_article_id)
        assert data["title"] == updated_title


def test_news_delete_request(client):
    mock_article_id = mock_ids[0]
    with client:
        r1 = client.delete(f"/api/v1/news/{mock_article_id}?api_key={API_KEY}")
        assert r1.status_code == 200

        r2 = client.get(f"/api/v1/news/{mock_article_id}")
        assert r2.status_code == 404
