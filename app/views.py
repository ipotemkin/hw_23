from flask_restx import Resource, Namespace, reqparse, inputs, fields
from flask_pydantic import validate
from app.models import BodyModel, QueryModel
from app.utils import read_line_from_file, run_cmd, execute_request
import os
from app.const import DATA_DIR, RATE_LIMIT
from app.limit import limiter

index_ns = Namespace("perform_query", description="Выполнить запрос")

parser = reqparse.RequestParser()
parser.add_argument("filter", type=str)  # a text to find
parser.add_argument("regex", type=str)  # a regular expression to find
parser.add_argument("limit", type=inputs.positive)  # a number of strings to output
parser.add_argument("sort", type=str, choices=("asc", "desc"))  # <asc:desc>
parser.add_argument("map", type=inputs.positive)  # a column number to output
parser.add_argument("unique", type=bool)  # outputs only unique values
parser.add_argument(
    "filename", type=str, required=True, default="apache_logs.txt"
)  # a file to process

my_fields = index_ns.model(
    "BodyModel",
    {
        "filename": fields.String(
            description="Имя файла", required=True, default="apache_logs.txt"
        ),
        "cmd1": fields.String(
            description="Первая команда",
            enum=["filter", "limit", "map", "sort", "unique", "regex"],
        ),
        "value1": fields.String(description="Значение первой команды"),
        "cmd2": fields.String(
            description="Вторая команда",
            enum=["limit", "filter", "map", "sort", "unique"],
        ),
        "value2": fields.String(description="Значение второй команды"),
    },
)


@index_ns.route("/")
class IndexView(Resource):
    decorators = [limiter.limit(RATE_LIMIT)]

    @index_ns.doc(
        params={
            "filter": "Что ищем?",
            "regex": "Поиск по рег выражению",
            "limit": "Сколько срок выводим? (>0)",
            "sort": "Как сортируем? <asc:desc>",
            "map": "Какую колонку выводим? (>0)",
            "unique": "Выводим только уникальные значения",
            "filename": "Файл, с которым работаем",
        }
    )
    @index_ns.expect(parser)
    @validate()
    def get(self, query: QueryModel):
        return execute_request(query)

    @index_ns.doc(
        body=my_fields,
        description="""
**cmd1**, **cmd2** - команды
**value1**, **value2** – значения команд

**Список команд:**
**filter** – фильтрует список по переданной подстроке,
**limit** – ограничивает количество строк в выводе,
**map** – вывести колонку с указанным номером (первая колонка = 1),
**sort** – сортируем вывод <asc – по возрастанию, desc – по убыванию>,
**unique** – выводим только уникальные сроки

**Пример:**
{
'cmd1': 'filter',
'value1': 'POST',  # ищем подстроку POST
'cmd2': 'limit',
'value2': '5'  # выводим 5 строк
}
""",
    )
    @validate()
    def post(self, body: BodyModel):
        source = read_line_from_file(os.path.join(DATA_DIR, body.filename))
        res = run_cmd(source, body.cmd1.value, body.value1)
        return run_cmd(res, body.cmd2.value, body.value2)


# @index_ns.route("/text/")
# @index_ns.expect(parser)
# @validate()
# @limiter.limit("1/hour")
# def get_data(query: QueryModel):
#     return execute_request(query)
