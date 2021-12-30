from utils import MyIndexError
from app import app, api


@api.errorhandler(MyIndexError)
def index_error(e):
    print("I am in index_error")
    return {"error": "Index Error", "message": "The column number is out of range"}, 400


if __name__ == "__main__":
    app.run()
