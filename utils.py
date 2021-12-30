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
        while True:
            try:
                yield next(f)
            except StopIteration:
                break


# string_split = re.split('"\s"|"\s|\s"|(\[\])|\s-\s-\s', string)


def split_str(text: str) -> list:
    text_split = re.split('"\s"|"\s|\s"|(\[\])|\s-\s-\s', text)  # noqa
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
        raise IndexError
    return split_text[column - 1]


def get_strings(source: Generator, column: int = None, limit: int = None) -> list:
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


def find_substring(
    source: Generator, substring: str, column: int = None, limit: int = None
) -> list:
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
    it = iter(read_line_from_file("./data/apache_logs.txt"))
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
