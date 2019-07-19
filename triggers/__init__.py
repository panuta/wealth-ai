from flask import Blueprint
from . import fetch_stock


trigger_bp = Blueprint('trigger', __name__, url_prefix='/trigger')
