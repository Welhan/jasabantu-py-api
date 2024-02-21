from flask import Blueprint, jsonify, request
from models.mitraModels import Mitra
from helpers.helpers import *

import bcrypt

mitra_model = Mitra()

mitra_bp = Blueprint('mitra_bp', __name__)





