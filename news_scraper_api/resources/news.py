from flask import Response
from flask_restful import Resource, abort, request
from mongoengine.errors import NotUniqueError, ValidationError
from bson.errors import InvalidId

from core.parsers import post_parser
from core.utils import api_key_required, get_object_or_404
from models.article import Article


class News(Resource):
    def get(self, id=None):
        # /api/v1/news/`article_id`
        if id:
            try:
                article = get_object_or_404(Article, id=id)
            except (ValidationError, InvalidId) as e:
                abort(502, message=e.message)

            return Response(article.to_json(), mimetype="application/json")

        # /api/v1/news?source=`source_name`
        if source_name := request.args.get("source", None):
            news_from_source = (
                Article.objects(source_name__iexact=source_name)
                .order_by("-created")
                .to_json()
            )
            return Response(news_from_source, mimetype="application/json")

        # /api/v1/news
        news = Article.objects.order_by("-created").to_json()
        return Response(news, mimetype="application/json")

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
        try:
            article = get_object_or_404(Article, id=id)
        except (ValidationError, InvalidId) as e:
            abort(502, message=e.message)

        article.update(**payload)
        updated_article = Article.objects.get(id=id).to_json()

        return Response(updated_article, mimetype="application/json")

    @api_key_required
    def delete(self, id):
        article = get_object_or_404(Article, id=id)
        article.delete()
        return 200
