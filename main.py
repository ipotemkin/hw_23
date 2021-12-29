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
@index_ns.doc(params={
    "filter": "Что ищем?",
    "limit": "Сколько срок выводим?",
    "sort": "Как сортируем? <asc:desc>",
    "map": "Какую колонку выводим?",
    "unique": "Выводим только уникальные значения",
    "filename": "Файл, с которым работаем",
})
class IndexView(Resource):
    @api.expect(parser)
    def post(self):
        params_dict = parser.parse_args()

        cmd_filter = params_dict["filter"]
        cmd_limit = params_dict["limit"]
        cmd_sort = params_dict["sort"]
        cmd_map = params_dict["map"]
        cmd_unique = params_dict["unique"]
        filename = params_dict["filename"]

        return {k: v for k, v in params_dict.items() if v is not None}

        # return f"filter={cmd_filter}, limit={cmd_limit}, sort={cmd_sort}," \
        #        f" map={cmd_map}, unique={cmd_unique}, filename={filename}"

        # return request.args
        # return "<h1>Here will be your query results<h1>"


if __name__ == "__main__":
    app.run()
