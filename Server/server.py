from sftpserver import start_server
from flask import Flask, request
from flask_restful import reqparse, Resource, Api
from sqlalchemy import create_engine
from json import dumps


HOST, PORT = 'localhost', 3373
app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
parser.add_argument('key')
parser.add_argument('id')


class Key(Resource):
    def post(self):
        args = parser.parse_args()
        f = open('./key/'+ args['id'] + '.key', 'w+')
        f.write(args['key'])
        f.close()

        return {'status': 'success'}, 201
class StartServer(Resource):
    def post(self):
        args = parser.parse_args()
        print('./key/'+args['id']+'.key')
        start_server(HOST, PORT, './key/1234.key', 'DEBUG')
        return {'status': 'success'}, 201


api.add_resource(Key, '/')
api.add_resource(StartServer, '/StartServer')

def main():
    start_server(HOST, PORT, './key/backup.key', 'DEBUG')
if __name__ == '__main__':
    app.run()
    #main()