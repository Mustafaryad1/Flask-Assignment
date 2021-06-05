# blueprints/documented_endpoints/__init__.py
from flask import Blueprint
from flask_restplus import Api
from foodSystem.documented_endpoints.hello import namespace as hello_world_ns

blueprint = Blueprint('swagger', __name__, url_prefix='/swagger')

api_extension = Api(
    blueprint,
    title='Food System RESTfull API demo',
    version='1.0',
    description='Food delivery application where restaurants can upload their \
menu online and enable users to place orders to be delivered to their locations.',
    doc='/doc'
)

api_extension.add_namespace(hello_world_ns)