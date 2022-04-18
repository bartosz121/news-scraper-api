from flask_restful import reqparse


class RequestParser(reqparse.RequestParser):
    def parse_args(self, req=None, strict=False, http_error_code=400):
        """Base method not changed. Used to remove 'api_key' from namespace"""
        namespace = super().parse_args(req, strict, http_error_code)
        namespace.pop("api_key")
        return namespace


post_parser = RequestParser()
post_parser.add_argument("title", type=str, help="Article title", required=True)
post_parser.add_argument(
    "source_name", type=str, help="Article source name.", required=True
)
post_parser.add_argument(
    "source_unique_id",
    type=str,
    help="Article source unique id. Id used by article provider.",
    required=True,
)
post_parser.add_argument("url", type=str, help="Article url", required=True)
post_parser.add_argument("img_url", type=str, help="Article image url")
post_parser.add_argument("description", type=str, help="Article description")
post_parser.add_argument("api_key", type=str, help="API Key")
