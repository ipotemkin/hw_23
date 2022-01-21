from flask import Flask
from flask_restx import Api
from app.views import index_ns
from app.limit import limiter

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config["JSON_AS_ASCII"] = False

api = Api(
    app,
    version="1.1.0",
    title="Log tools API",
    description="Homework 23 with SkyPro's Python Dev Course",
    contact="Igor Potemkin",
    contact_email="ipotemkin@rambler.ru",
)
api.add_namespace(index_ns)

limiter.init_app(app)
