from flask import Blueprint, jsonify, Flask, request
from flaskext.mysql import MySQL
doctor_api_bp = Blueprint('doctor_api',__name__,template_folder='templates')

app = Flask(__name__)
app.config.from_envvar('NOALPHA_SETTINGS')
mysql = MySQL()
mysql.init_app(app)

@doctor_api_bp.route('/')
def index():
    return jsonify(message='Welcome to doctor_api\'s index page.')

@doctor_api_bp.route('/test-config')
def testConfig():
    return app.config['APP_NAME']

@doctor_api_bp.route('/put-tokens', methods=['POST'])
def putTokens():
    con = mysql.connect()
    cursor = con.cursor()
    cursor.execute('insert into tokens (serial_no, start_time, status, doctor_location_id) values (1, \'' + request.form['start_time'] + '\', \'empty\', ' + request.form['doctor_location_id'] + ')')
    con.commit()
    return jsonify(message='success')