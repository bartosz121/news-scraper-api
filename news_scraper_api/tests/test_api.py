import os
import json
import pytest
from dotenv import load_dotenv
from mongoengine import connect, disconnect
from werkzeug.exceptions import HTTPException

from news_scraper_api import config
from news_scraper_api.app import create_app
from news_scraper_api.core.utils import get_object_or_404, get_page_number
from news_scraper_api.models.article import Article
from news_scraper_api.resources.news import ITEMS_PER_PAGE
from news_scraper_api.tests.mock_data import mock_articles

load_dotenv()

API_KEY = os.getenv("API_KEY")

mock_ids = []

post_request_data = {
    "title": "Title 99",
    "source_name": "BBC",
    "source_unique_id": "id99",
    "url": "url99",
    "img_url": "img_url99",
    "description": "description99",
}


@pytest.fixture(scope="module")
def db():
    connect("mongomockdb", host="mongomock://localhost")
    for a in mock_articles:
        a = Article(**a).save()
        mock_ids.append(a.id)

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


def test_valid_get_page_number(client):
    with client:
        r_valid = client.get("/api/v1/news?page=2")
        assert r_valid.status_code == 200


def test_invalid_get_page_number(client):
    with client:
        r_invalid_1 = client.get("/api/v1/news?page=-1")
        assert r_invalid_1.status_code == 400

        r_invalid_2 = client.get("/api/v1/news?page=12page22")
        assert r_invalid_2.status_code == 400

        r_invalid_3 = client.get("/api/v1/news?page=two")
        assert r_invalid_3.status_code == 400


# Tests for "/api/v1/news/"


def test_get_news(client):
    """/api/v1/news"""
    expected_length = 10  # ITEMS_PER_PAGE; we have 12 articles in mock data
    with client:
        r = client.get("/api/v1/news")
        assert r.status_code == 200

        data = r.get_json()
        data_result = json.loads(data["result"])

        assert len(data_result) == expected_length

        # Remember that this endpoint sorts articles by `-created`
        assert all(
            [
                str(expected_id) == article["id"]
                for expected_id, article in zip(mock_ids, data_result)
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
    """/api/v1/news?source=bbc"""
    source_name = "BBC"
    expected_length = len([a for a in mock_articles if a["source_name"] == source_name])

    with client:
        r = client.get(f"/api/v1/news?source={source_name}")
        assert r.status_code == 200

        data = r.get_json()
        data_result = json.loads(data["result"])

        assert len(data_result) == expected_length


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

        # update post_request_data with id to delete it in `test_news_delete_request`
        post_request_data["id"] = data["id"]

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
    with client:
        r1 = client.delete(f"/api/v1/news/{post_request_data['id']}?api_key={API_KEY}")
        assert r1.status_code == 200

        r2 = client.get(f"/api/v1/news/{post_request_data['id']}")
        assert r2.status_code == 404


def test_pagination_hasNext_is_true(client):
    expected_result = True
    with client:
        r = client.get("/api/v1/news")
        assert r.status_code == 200

        data = r.get_json()

        assert data["hasNext"] == expected_result


def test_pagination_hasNext_is_false(client):
    expected_result = False
    with client:
        r = client.get("/api/v1/news?page=2")
        assert r.status_code == 200

        data = r.get_json()

        # There are 12 articles in mock data so hasNext should be False
        assert data["hasNext"] == expected_result


def test_pagination_result(client):
    expected_page_1 = mock_ids[:ITEMS_PER_PAGE]
    expected_page_2 = mock_ids[ITEMS_PER_PAGE:]

    with client:
        r_1 = client.get("/api/v1/news")
        assert r_1.status_code == 200

        data = r_1.get_json()
        data_result_page_1 = json.loads(data["result"])

        assert all(
            [
                str(expected_id) == article["id"]
                for expected_id, article in zip(expected_page_1, data_result_page_1)
            ]
        )

        # page 2
        r_2 = client.get("/api/v1/news?page=2")
        assert r_2.status_code == 200

        data = r_2.get_json()
        data_result_page_2 = json.loads(data["result"])

        assert all(
            [
                str(expected_id) == article["id"]
                for expected_id, article in zip(expected_page_2, data_result_page_2)
            ]
        )
