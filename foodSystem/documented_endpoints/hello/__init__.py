from flask import request
from flask_restplus import Namespace, Resource, fields

namespace = Namespace('home', 'Authentication related endpoints')

hello_world_model = namespace.model('User', {
    'message': fields.String(
        readonly=True,
        description='Hello world message'
    )
})

hello_world_example = {'message': 'Hello World!'}

@namespace.route('')
class User(Resource):

    @namespace.marshal_list_with(hello_world_model)
    @namespace.response(500, 'Internal Server error')
    def get(self):
        '''Hello world message endpoint'''

        return hello_world_example