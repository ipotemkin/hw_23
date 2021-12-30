from flask import Flask
from flask_restx import reqparse, Api, Resource, inputs
from utils import read_line_from_file, find_subsring, make_unique_lst, get_strings

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
parser.add_argument("limit", type=inputs.positive)  # a number of strings to output
parser.add_argument("sort", type=str, choices=('asc', 'desc'))  # <asc:desc>
parser.add_argument("map", type=inputs.positive)  # a column number to output
parser.add_argument("unique", type=str)  # outputs only unique values
parser.add_argument("filename", type=str, required=True)  # a file to process

# input_model = api.Model("InputModel")


# @app.route('/')
# def index():
#     return "<h1>Homework 23: Functional Programming<h1>"


# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# DATA_DIR = os.path.join(BASE_DIR, "data")
#
#
# @app.route("/perform_query")
# def perform_query():
#     # получить параметры query и file_name из request.args, при ошибке вернуть ошибку 400
#     # проверить, что файла file_name существует в папке DATA_DIR, при ошибке вернуть ошибку 400
#     # с помощью функционального программирования (функций filter, map), итераторов/генераторов сконструировать запрос
#     # вернуть пользователю сформированный результат
#     return app.response_class('', content_type="text/plain")


@index_ns.route("/")
@index_ns.doc(params={
    "filter": "Что ищем?",
    "limit": "Сколько срок выводим?",
    "sort": "Как сортируем? <asc:desc>",
    "map": "Какую колонку выводим? (>0)",
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

        # return {k: v for k, v in params_dict.items() if v is not None}

        source = read_line_from_file("./data/" + filename)

        rev_order = False if cmd_sort == "asc" else True

        if cmd_filter:
            if cmd_unique:
                if cmd_sort:
                    return sorted(
                        list(set(find_subsring(source, cmd_filter, cmd_map))), reverse=rev_order
                    )[:cmd_limit]
                return list(set(find_subsring(source, cmd_filter, cmd_map)))[:cmd_limit]

            if cmd_sort:
                return sorted(find_subsring(source, cmd_filter, cmd_map), reverse=rev_order)[:cmd_limit]
            return find_subsring(source, cmd_filter, cmd_map, cmd_limit)

        if cmd_unique:
            if cmd_sort:
                return sorted(make_unique_lst(source, column=cmd_map), reverse=rev_order)[:cmd_limit]
            return make_unique_lst(source, column=cmd_map, limit=cmd_limit)

        if cmd_sort:
            return sorted(get_strings(source, column=cmd_map), reverse=rev_order)[:cmd_limit]
        return get_strings(source, column=cmd_map, limit=cmd_limit)

        # return f"filter={cmd_filter}, limit={cmd_limit}, sort={cmd_sort}," \
        #        f" map={cmd_map}, unique={cmd_unique}, filename={filename}"

        # return request.args
        # return "<h1>Here will be your query results<h1>"


if __name__ == "__main__":
    app.run()
