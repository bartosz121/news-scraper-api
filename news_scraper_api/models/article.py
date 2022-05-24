from datetime import datetime
from core.db import mongo
import mongoengine_goodjson as gj


class Article(gj.Document):
    title = mongo.StringField(required=True)
    source_name = mongo.StringField(required=True)
    source_unique_id = mongo.StringField(required=True, unique=True)
    url = mongo.StringField(required=True)
    img_url = mongo.StringField()
    description = mongo.StringField()
    created = mongo.DateTimeField(default=datetime.utcnow)

    meta = {
        "indexes": [
            {
                "fields": [
                    "$title",
                ],
                "default_language": "english",
            }
        ]
    }
