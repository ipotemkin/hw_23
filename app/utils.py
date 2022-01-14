import os
import re
from typing import Generator, Union, List
from flask import abort
from app.models import QueryModel
from app.errors import MyIndexError, RowNumberError
from app.const import DATA_DIR


def read_line_from_file(file_path):
    try:
        with open(file_path) as f:
            while True:
                try:
                    yield next(f)
                except StopIteration:
                    break
    except FileNotFoundError:
        abort(400, "File not fund")


def split_str(text: str) -> list:
    text_split = re.split(r'"\s"|"\s|\s"|(\[\])|\s-\s-\s', text)  # noqa
    return [item.strip() for item in text_split if item]


def get_column(text: str, column: int) -> str:
    """
    returns the value of the column with number column
    :param text: a string
    :param column: a column number
    :return: the value of the column with the specified number
    """
    split_text = split_str(text)
    if column > len(split_text):
        raise MyIndexError
    return split_text[column - 1]


def get_strings(source: Generator, column: int = None, limit: int = None) -> list:
    result_lst: List[str] = []
    for line in source:
        if column:
            line = get_column(line, column)
        if limit and not (len(result_lst) < limit):
            break
        result_lst.append(line)
    return result_lst


def make_unique_lst(source: Generator, column: int = None, limit: int = None) -> list:
    if not column:
        return list(set([line for line in source]))[:limit]
    return list(set([get_column(line, column) for line in source]))[:limit]


def find_substring(
    source: Generator, substring: str, column: int = None, limit: int = None
) -> list:
    result_lst: List[str] = []
    for line in source:
        if column:
            line = get_column(line, column)
        if substring in line:
            if limit and not (len(result_lst) < limit):
                break
            result_lst.append(line)
    return result_lst


def find_regex(
    source: Generator, substring: str, column: int = None, limit: int = None
) -> list:
    result_lst: List[str] = []
    for line in source:
        if column:
            line = get_column(line, column)
        if re.search(substring, line):
            if limit and not (len(result_lst) < limit):
                break
            result_lst.append(line)
    return result_lst


def run_cmd(source: Union[Generator, list], cmd: str, value: str) -> List[str]:
    res: List[str] = []
    if cmd == "filter":
        res = list(filter(lambda x: value in x, source))
    if cmd == "limit":
        try:
            rows = int(value)
        except ValueError:
            raise RowNumberError
        if rows < 1:
            raise RowNumberError
        res = list(source)[:rows]
    if cmd == "unique":
        res = list(set(source))
    if cmd == "sort":
        rev_order = False if value == "asc" else True
        res = sorted(source, reverse=rev_order)
    if cmd == "map":
        if (index := int(value)) < 1:
            raise MyIndexError
        try:
            res = list(map(lambda x: split_str(x)[index - 1], source))
        except IndexError:
            raise MyIndexError
    if cmd == "regex":
        res = list(filter(lambda x: re.search(value, x), source))
    return res


def execute_request(query: QueryModel) -> list:
    source = read_line_from_file(os.path.join(DATA_DIR, query.filename))
    rev_order = False if query.sort == "asc" else True

    if query.regex:
        if query.unique:
            if query.sort:
                return sorted(
                    list(set(find_regex(source, query.regex, query.map))),
                    reverse=rev_order,
                )[: query.limit]
            return list(set(find_substring(source, query.regex, query.map)))[
                : query.limit
            ]

        if query.sort:
            return sorted(
                find_regex(source, query.regex, query.map), reverse=rev_order
            )[: query.limit]
        return find_regex(source, query.regex, query.map, query.limit)

    if query.filter:
        if query.unique:
            if query.sort:
                return sorted(
                    list(set(find_substring(source, query.filter, query.map))),
                    reverse=rev_order,
                )[: query.limit]
            return list(set(find_substring(source, query.filter, query.map)))[
                : query.limit
            ]

        if query.sort:
            return sorted(
                find_substring(source, query.filter, query.map), reverse=rev_order
            )[: query.limit]
        return find_substring(source, query.filter, query.map, query.limit)

    if query.unique:
        if query.sort:
            return sorted(make_unique_lst(source, column=query.map), reverse=rev_order)[
                : query.limit
            ]
        return make_unique_lst(source, column=query.map, limit=query.limit)

    if query.sort:
        return sorted(get_strings(source, column=query.map), reverse=rev_order)[
            : query.limit
        ]
    return get_strings(source, column=query.map, limit=query.limit)


# just for testing
if __name__ == "__main__":
    it = iter(read_line_from_file("../data/apache_logs.txt"))
    string = next(it)
    print(string)
    # column = get_column(string, 5)
    # print(column)
    #
    string_split = split_str(string)
    print(string_split)
    print(len(string_split))

    # print(*(line for line in read_line_from_file('./data/apache_logs.txt') if "17/May" in line))

    # i = 0
    # for line in read_line_from_file('./data/apache_logs.txt'):
    #     print(get_column(line, 1))
    #     i += 1
    # print(i, "lines")
    #
    # unique_lst = set([get_column(line, 1) for line in read_line_from_file('./data/apache_logs.txt')])
    # # print(*unique_lst, sep='\n')
    # print(len(unique_lst))

    # source = read_line_from_file("./data/apache_logs.txt")
    # print(*sorted(make_unique_lst(source, 1))[:10], sep="\n")

    # source = read_line_from_file('./data/apache_logs.txt')
    # print(*find_substring(source, "20/May/2015:17:05:55", 2), sep='\n')
