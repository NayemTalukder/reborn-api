from flask_restful import Resource, reqparse

class Home(Resource):
        def get(self):
            return 'API Home'