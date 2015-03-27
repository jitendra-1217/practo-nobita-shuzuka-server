from flask import Blueprint, jsonify, Flask
doctor_api_bp = Blueprint('doctor_api',__name__,template_folder='templates')

app = Flask(__name__)
app.config.from_envvar('NOALPHA_SETTINGS')

@doctor_api_bp.route('/')
def index():
    return jsonify(message='Welcome to doctor_api\'s index page.')

@doctor_api_bp.route('/test-config')
def testConfig():
    return app.config['APP_NAME']