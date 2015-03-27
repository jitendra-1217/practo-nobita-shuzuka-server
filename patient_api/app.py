from flask import Blueprint, jsonify, Flask
patient_api_bp = Blueprint('patient_api',__name__,template_folder='templates')

app = Flask(__name__)
app.config.from_pyfile('../flaskapp.cfg')

@patient_api_bp.route('/')
def index():
    return jsonify(message='Welcome to patient_api\'s index page.')
