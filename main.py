from flask import Flask
from flask_restx import reqparse, Api, Resource

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config["JSON_AS_ASCII"] = False

api = Api(
    app,
    version="0.1.0",
    title="Log tools API",
    description="Homework 23 with SkyPro's Python Dev Course",
    contact="Igor Potemkin",
    contact_email="ipotemkin@rambler.ru",
)
index_ns = api.namespace("perform_query")
parser = reqparse.RequestParser()
parser.add_argument("filter", type=str)  # a text to find
parser.add_argument("limit", type=int)  # a number of strings to output
parser.add_argument("sort", type=str)  # <asc:desc>
parser.add_argument("map", type=int)  # a column number to output
parser.add_argument("unique", type=str)  # outputs only unique values
parser.add_argument("filename", type=str)  # a file to process


# @app.route('/')
# def index():
#     return "<h1>Homework 23: Functional Programming<h1>"


@index_ns.route("/")
class IndexView(Resource):
    @api.expect(parser)
    def post(self):
        cmd_filter = parser.parse_args()["filter"]
        cmd_limit = parser.parse_args()["limit"]
        cmd_map = parser.parse_args()["map"]
        cmd_unique = parser.parse_args()["unique"]
        filename = parser.parse_args()["filename"]

        return f"filter={cmd_filter}, limit={cmd_limit}, map={cmd_map}, unique={cmd_unique}, filename={filename}"
        # return request.args
        # return "<h1>Here will be your query results<h1>"


if __name__ == "__main__":
    app.run()
