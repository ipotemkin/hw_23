import re
from typing import Generator


def find(file_path, txt):
    with open(file_path) as f:
        while True:
            try:
                line = next(f)
            except StopIteration:
                break
            if txt in line:
                yield line[:-1]


def read_line_from_file(file_path):
    with open(file_path) as f:
        # yield (line for line in f)
        while True:
            try:
                yield next(f)
            except StopIteration:
                break
            # if txt in line:
            #     yield line[:-1]


def split_str(string: str) -> list:
    string_split = re.split('"\s"|"\s|\s"|(\[\])|\s-\s-\s', string)
    return [item.strip() for item in string_split if item]


def get_column(string: str, column: int) -> str:
    string_split = split_str(string)
    if column > len(string_split):
        raise IndexError
    return string_split[column - 1]


def get_strings(source: Generator, column: int = None, limit: int = None):
    result_lst = []
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


def find_subsring(source: Generator, substring: str, column: int = None, limit: int = None) -> list:
    result_lst = []
    for line in source:
        if column:
            line = get_column(line, column)
        if substring in line:
            if limit and not (len(result_lst) < limit):
                break
            result_lst.append(line)
    return result_lst


if __name__ == "__main__":
    # it = iter(read_line_from_file('./data/apache_logs.txt'))
    # string = next(it)
    # print(string)
    # column = get_column(string, 5)
    # print(column)
    #
    # string_split = split_str(string)
    # print(string_split)
    # print(len(string_split))

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

    source = read_line_from_file('./data/apache_logs.txt')

    print(*sorted(make_unique_lst(source, 1))[:10], sep='\n')

    # source = read_line_from_file('./data/apache_logs.txt')
    # print(*find_subsring(source, "20/May/2015:17:05:55", 2), sep='\n')
