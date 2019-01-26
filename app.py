from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask import render_template

from temp_check.temp_converter import TempConverter

app = Flask(__name__,  static_url_path='/static')
api = Api(app)


parser = reqparse.RequestParser()
parser.add_argument('starting_value')
parser.add_argument('desired_unit')
parser.add_argument('student_answer')


class CheckTemp(Resource):

    def post(self):
        args = parser.parse_args()
        return {
            'answer': TempConverter.check_conversion(
                starting_value=args['starting_value'],
                student_answer=args['student_answer'],
                desired_unit=args['desired_unit']
            )
        }

class FavIcon(Resource):
    def get(self):
        return {}


api.add_resource(CheckTemp, '/check_temp/')
api.add_resource(FavIcon, '/favicon.ico')


@app.route('/')
def index(name=None):
    return render_template('index.html', name=name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
