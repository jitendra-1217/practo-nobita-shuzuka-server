from flask import Blueprint, jsonify, Flask, request
from flaskext.mysql import MySQL
import datetime
doctor_api_bp = Blueprint('doctor_api',__name__,template_folder='templates')

app = Flask(__name__)
mysql = MySQL()
mysql.init_app(app)
app.config.from_pyfile('../flaskapp.cfg')

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
    cursor.execute('select avg_checkup_time from doctors where id in (select doctor_id from doctor_locations where id = "%d")' % (int(request.form['doctor_location_id'])))
    data = cursor.fetchone()
    avgCheckupTimeInMin = str(data[0])
    startTime = request.form['start_time']
    for serialNo in range(1, int(request.form['no_of_tokens']) + 1):
        cursor.execute('insert into tokens (serial_no, start_time, status, doctor_location_id) values ("%d", "%s", "empty", "%d")' % (serialNo, startTime, int(request.form['doctor_location_id'])))
        startTime = (datetime.datetime.strptime(startTime, "%H:%M:%S") + datetime.timedelta(minutes = int(avgCheckupTimeInMin))).strftime("%H:%M:%S")
    con.commit()
    return jsonify(message='success')
