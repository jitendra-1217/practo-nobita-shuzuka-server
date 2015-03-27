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

@patient_api_bp.route('/aquire-token', methods=['POST'])
def aquireToken():
    cursor.execute('select id from tokens where doctor_location_id = "%d" and status = "empty" limit 1' % (int(request.form['doctor_location_id'])))
    data = cursor.fetchone()
    if data is None:
        return jsonify(status='failed')
    id = str(data[0])
    cursor.execute('update tokens set patient_id = "%d", status = "assigned" where id = "%d"' % (int(request.form['patient_id']), int(id)))
    conn.commit()
    return jsonify(status='success', token_id=id)

@patient_api_bp.route('/list-doctor-locations', methods=['GET'])
def listDoctorLocations():
    cursor.execute('select id, latitude, longitude from doctor_locations where id in (select doctor_location_id from tokens where token_timestamp = "%s" group by doctor_location_id)' % (request.args.get('token_timestamp')))
    results = cursor.fetchall()
    resultsToReturn = []
    for result in results:
        resultsToReturn.append({'id':result[0], 'latitude':str(result[1]), 'longitude':str(result[2])})
    return jsonify(status='success',message=resultsToReturn)

@patient_api_bp.route('/details-of-doctor-location', methods=['GET'])
def detailsOfDoctorLocation():
    pass

@patient_api_bp.route('/status-of-token')
def statusOfToken():
    pass
