from flask import Blueprint, request, make_response, jsonify,render_template,redirect,url_for
import jwt
import datetime
from models import User, Note
from functools import wraps
from werkzeug.security import generate_password_hash,check_password_hash
from app import db
from sqlalchemy.orm import validates


views=Blueprint('views', __name__)




