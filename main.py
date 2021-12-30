from app.utils import MyIndexError
from app.app import app, api


@api.errorhandler(MyIndexError)
def index_error(e):
    return {"error": "Index Error", "message": "The column number is out of range"}, 400


if __name__ == "__main__":
    app.run()
