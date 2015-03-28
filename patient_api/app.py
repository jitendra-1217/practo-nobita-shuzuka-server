from flask import Blueprint, jsonify, Flask, request
from flaskext.mysql import MySQL
import datetime
patient_api_bp = Blueprint('patient_api',__name__,template_folder='templates')

app = Flask(__name__)
mysql = MySQL()
mysql.init_app(app)
app.config.from_pyfile('../flaskapp.cfg')
conn = mysql.connect()
cursor = conn.cursor()

@patient_api_bp.route('/')
def index():
    return jsonify(message='Welcome to patient_api\'s index page.')

@patient_api_bp.route('/acquire-token', methods=['POST'])
def aquireToken():
    cursor.execute('select id, serial_no from tokens where doctor_location_id = "%d" and status = "empty" limit 1' % (int(request.form['doctor_location_id'])))
    data = cursor.fetchone()
    if data is None:
        return jsonify(status='failed')
    id = str(data[0])
    tokenSerialNo = str(data[1])
    cursor.execute('update tokens set patient_id = "%d", status = "assigned" where id = "%d"' % (int(request.form['patient_id']), int(id)))
    conn.commit()
    return jsonify(status='success', token_id=id, tkoen_serial_no=tokenSerialNo)

@patient_api_bp.route('/list-doctor-locations', methods=['GET'])
def listDoctorLocations():
    cursor.execute('select id, latitude, longitude from doctor_locations where id in (select doctor_location_id from tokens group by doctor_location_id)')
    results = cursor.fetchall()
    resultsToReturn = []
    for result in results:
        resultsToReturn.append({'id':result[0], 'latitude':str(result[1]), 'longitude':str(result[2])})
    return jsonify(status='success',message=resultsToReturn)

@patient_api_bp.route('/details-of-doctor-location', methods=['POST'])
def detailsOfDoctorLocation():
    cursor.execute('select d.id, d.name, d.phone_no, d.avg_checkup_time, dl.landmark, dl.locality, dl.city, dl.country, dl.latitude, dl.longitude from doctors d right join doctor_locations dl on d.id = dl.doctor_id where dl.id = "%d"' % (int(request.form['doctor_location_id'])))
    result = cursor.fetchone()
    cursor.execute('select count(*) from tokens where doctor_location_id = "%d" and token_timestamp = "%s"' % (int(request.form['doctor_location_id']), request.form['token_timestamp']))
    totalTokenCount = str(cursor.fetchone()[0])
    cursor.execute('select count(*) from tokens where doctor_location_id = "%d" and token_timestamp = "%s" and status = "empty"' % (int(request.form['doctor_location_id']), request.form['token_timestamp']))
    emptyTokenCount = str(cursor.fetchone()[0])
    doctorLocationAddress = []
    for index in range(4,8):
        if result[index] is not None:
            doctorLocationAddress.append(result[index])
    doctorLocationAddress = ','.join(doctorLocationAddress)
    resultsToReturn = {'doctor_id':result[0], 'doctor_name':result[1], 'doctor_phone_no':result[2], 'doctor_avg_checkup_time':result[3], 'address':doctorLocationAddress, 'doctor_location_latitude': str(result[8]), 'doctor_location_longitude': str(result[9]), 'total_token_count': totalTokenCount, 'empty_token_count': emptyTokenCount}
    return jsonify(status='success',message=resultsToReturn)

@patient_api_bp.route('/status-of-token', methods=['POST'])
def statusOfToken():
    cursor.execute('select serial_no, token_timestamp, doctor_location_id from tokens where id = "%d"' % (int(request.form['id'])))
    result = cursor.fetchone()
    serialNo = str(result[0])
    tokenTimestamp = str(result[1])
    doctorLocationId = str(result[2])
    cursor.execute('select count(*) from tokens where token_timestamp = "%s" and doctor_location_id = "%d" and serial_no < "%d" and status not in ("assigned", "canceled by doctor")' % (tokenTimestamp, int(doctorLocationId), int(serialNo)))
    result = cursor.fetchone()
    beforeYou = str(result[0])
    resultsToReturn = {'before_you':beforeYou, 'expected_time':(datetime.datetime.now() + datetime.timedelta(minutes = 5*int(beforeYou))).strftime("%H:%M:%S")}
    return jsonify(status='success',message=resultsToReturn)
