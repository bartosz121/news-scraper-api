from typing import Type
from flask import Blueprint, Flask
from flask_restful import Api

from config import get_config, Config
from core.db import mongo
from resources.news import News


def create_app(config_obj: Type[Config]):
    app = Flask(__name__)
    app.config.from_object(config_obj)

    if not config_obj.TESTING:
        mongo.init_app(app)

    api_bp = Blueprint("api", __name__)
    api = Api(api_bp)

    api.add_resource(News, "/api/v1/news", "/api/v1/news/<string:id>")

    app.register_blueprint(api_bp)

    return app


if __name__ == "__main__":
    config_obj = get_config()
    app = create_app(config_obj)
    app.run()
