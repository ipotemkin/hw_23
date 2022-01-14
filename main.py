from app.errors import MyIndexError, RowNumberError, MyFileNotFoundError
from app.app import app, api


@api.errorhandler(MyIndexError)
def index_error(e):
    return {"error": "Index Error", "message": "The column number is out of range"}, 400


@api.errorhandler(RowNumberError)
def row_number_error(e):
    return {
        "error": "Row Number Error",
        "message": "The row number should be int and more than 0",
    }, 400


@api.errorhandler(MyFileNotFoundError)
def my_file_not_found_error(e):
    return {
        "error": "File Not Found Error",
        "message": "The specified file is not found",
    }, 400


if __name__ == "__main__":
    app.run()
