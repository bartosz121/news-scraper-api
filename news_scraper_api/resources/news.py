from flask import Response
from flask_restful import Resource, abort, request
from mongoengine.errors import NotUniqueError

from core.parsers import post_parser
from core.utils import api_key_required, get_object_or_abort, get_page_number
from models.article import Article


ITEMS_PER_PAGE = 10


class News(Resource):
    def get(self, id=None):
        # /api/v1/news/`article_id`
        if id:
            article = get_object_or_abort(Article, id=id)
            return Response(article.to_json(), mimetype="application/json")

        # /api/v1/news?source=`source_name`
        if source_name := request.args.get("source", None):
            news_qs = Article.objects(source_name__iexact=source_name).order_by(
                "-created"
            )
        # /api/v1/news?search=search%20by
        elif search_by := request.args.get("search", None):
            news_qs = Article.objects.search_text(search_by).order_by("$text_score")
        else:
            # /api/v1/news
            news_qs = Article.objects.order_by("-created")

        item_count = news_qs.count()
        page = get_page_number()
        offset = (page - 1) * ITEMS_PER_PAGE

        data = {
            "result": news_qs.skip(offset).limit(ITEMS_PER_PAGE).to_json(),
            "hasNext": True if (offset + ITEMS_PER_PAGE) <= item_count else False,
            "pageNumber": page,
        }

        return data

    @api_key_required
    def post(self):
        payload = post_parser.parse_args(strict=True)
        try:
            article = Article(**payload).save()
        except NotUniqueError:
            abort(
                409,
                message=f"Article with {payload['source_unique_id']!r} source unique id already in database",
            )

        added_article = Article.objects.get(id=article.id).to_json()
        return Response(added_article, mimetype="application/json", status=201)

    @api_key_required
    def put(self, id):
        payload = post_parser.parse_args(strict=True)
        article = get_object_or_abort(Article, id=id)

        article.update(**payload)
        updated_article = Article.objects.get(id=id).to_json()

        return Response(updated_article, mimetype="application/json")

    @api_key_required
    def delete(self, id):
        article = get_object_or_abort(Article, id=id)
        article.delete()
        return 200
