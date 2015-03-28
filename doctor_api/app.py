from flask import Blueprint, jsonify, Flask, request
from flaskext.mysql import MySQL
import datetime
doctor_api_bp = Blueprint('doctor_api',__name__,template_folder='templates')

app = Flask(__name__)
mysql = MySQL()
mysql.init_app(app)
app.config.from_pyfile('../flaskapp.cfg')
conn = mysql.connect()
cursor = conn.cursor()

@doctor_api_bp.route('/')
def index():
    return jsonify(message='Welcome to doctor_api\'s index page.')

@doctor_api_bp.route('/test-config')
def testConfig():
    return app.config['APP_NAME']

@doctor_api_bp.route('/put-tokens', methods=['POST'])
def putTokens():
    cursor.execute('select avg_checkup_time from doctors where id in (select doctor_id from doctor_locations where id = "%d")' % (int(request.form['doctor_location_id'])))
    data = cursor.fetchone()
    cursor.execute('select * from tokens where token_timestamp = "%s" and doctor_location_id = "%d"' % (request.form['token_timestamp'], int(request.form['doctor_location_id'])))
    datatokens = cursor.fetchone()
    if not datatokens:
        avgCheckupTimeInMin = str(data[0])
        startTime = request.form['start_time']
        for serialNo in range(1, int(request.form['no_of_tokens']) + 1):
            cursor.execute('insert into tokens (serial_no, token_timestamp, start_time, status, doctor_location_id) values ("%d", "%s", "%s", "empty", "%d")' % (serialNo, request.form['token_timestamp'], startTime, int(request.form['doctor_location_id'])))
            startTime = (datetime.datetime.strptime(startTime, "%H:%M:%S") + datetime.timedelta(minutes = int(avgCheckupTimeInMin))).strftime("%H:%M:%S")
        conn.commit()
        return jsonify(status='success')
    else:
        return jsonify(status='duplicate')

@doctor_api_bp.route('/update-token', methods=['POST'])
def updateToken():
    cursor.execute('update tokens set status = "%s" where id = "%d"' % (request.form['status'], int(request.form['id'])))
    conn.commit()
    return jsonify(status='success')

@doctor_api_bp.route('/list-tokens', methods=['POST'])
def listTokens():
    cursor.execute('select t.id, t.serial_no, t.start_time, t.status, p.id, p.name, p.phone_no, t.booking_reason from tokens t left join patients p on t.patient_id = p.id where doctor_location_id = "%d" and token_timestamp = "%s"' % (int(request.form['doctor_location_id']), request.form['token_timestamp']))
    results = cursor.fetchall()
    resultsToReturn = []
    for result in results:
        resultsToReturn.append({'token_id':result[1], 'token_serial_no':result[1], 'token_start_time':str(result[2]), 'token_status':result[3], 'patient_id':result[4], 'patient_name':result[5], 'patient_phone_no':result[6], 'booking_reason':result[7]})
    return jsonify(status='success',message=resultsToReturn)

@doctor_api_bp.route('/remain-tokens', methods=['POST'])
def remainTokens():
    cursor.execute('select t.id, t.serial_no, t.start_time, t.status, dl.latitude, dl.longitude, d.name from tokens t left join doctor_locations dl on t.doctor_location_id = dl.id left join doctors d on d.id = dl.doctor_id where doctor_location_id = "%d" and token_timestamp = "%s" and t.status = "empty"' % (int(request.form['doctor_location_id']), request.form['token_timestamp']))
    results = cursor.fetchall()
    resultsToReturn = []
    for result in results:
        resultsToReturn.append({'token_id':result[1], 'token_serial_no':result[1], 'token_start_time':str(result[2]), 'token_status':result[3], 'doctor_lat':result[4], 'doctor_long':result[5], 'doctor_name':result[6]})
    return jsonify(status='success',message=resultsToReturn)
