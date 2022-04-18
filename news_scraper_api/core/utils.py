import os
import functools
from flask import request
from flask_restful import abort
from mongoengine import errors


def api_key_is_valid(api_key):
    return api_key == os.getenv("API_KEY")


def api_key_required(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        api_key = request.args.get("api_key", None)
        if not api_key:
            return {"message": "Please provide an API Key"}, 401

        if api_key_is_valid(api_key):
            return func(*args, **kwargs)
        else:
            return {"message": "API Key not valid"}, 401

    return wrapper


def get_object_or_404(class_, *args, **kwargs):
    try:
        obj = class_.objects.get(*args, **kwargs)
    except errors.DoesNotExist as e:
        abort(404, message=f"{class_.__name__} not found.")
    else:
        return obj
