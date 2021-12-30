from flask_restx import Resource, Namespace, reqparse, inputs, fields
from flask_pydantic import validate
import json
from models import BodyModel, QueryModel
from utils import (
    read_line_from_file,
    run_cmd,
    execute_request
)
import os

index_ns = Namespace("perform_query", description="Выполнить запрос")

parser = reqparse.RequestParser()
parser.add_argument("filter", type=str)  # a text to find
parser.add_argument("limit", type=inputs.positive)  # a number of strings to output
parser.add_argument("sort", type=str, choices=("asc", "desc"))  # <asc:desc>
parser.add_argument("map", type=inputs.positive)  # a column number to output
parser.add_argument("unique", type=bool)  # outputs only unique values
parser.add_argument(
    "filename", type=str, required=True, default="apache_logs.txt"
)  # a file to process

my_fields = index_ns.model('BodyModel', {
    'filename': fields.String(description='Имя файла', required=True, default="apache_logs.txt"),
    'cmd1': fields.String(description='Первая команда', enum=["filter", "limit", "map", "sort", "unique"]),
    'value1': fields.String(description='Значение первой команды'),
    'cmd2': fields.String(description='Вторая команда', enum=["filter", "limit", "map", "sort", "unique"]),
    'value2': fields.String(description='Значение второй команды'),
})


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


@index_ns.route("/")
class IndexView(Resource):
    @index_ns.doc(
        params={
            "filter": "Что ищем?",
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

    @validate()
    @index_ns.doc(
        body=my_fields,
        description=
        """
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
"""
    )
    def post(self, body: BodyModel):
        source = read_line_from_file(os.path.join(DATA_DIR, body.filename))
        body_d = json.loads(body.json())  # to transform to a simple dictionary
        res = run_cmd(source, body_d["cmd1"], body_d["value1"])
        return run_cmd(res, body_d["cmd2"], body_d["value2"])
