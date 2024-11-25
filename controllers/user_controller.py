import hashlib
from flask import session
from models import db
from user.models.user import User
from config import Config

salt = Config.PASSWORD_HASH_SALT

def get_all_users():
    return User.query.all()

def create_user(first_name, last_name, email, phone, password):
    password = hash_password(password, salt)
    new_user = User(first_name=first_name, last_name=last_name, email=email, phone=phone, password=password)
    db.session.add(new_user)
    db.session.commit()

def hash_password(password, salt):
    password_hash = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
    return password_hash

def verify_password(stored_password, provided_password, salt):
    password_hash = hashlib.sha256((provided_password + salt).encode('utf-8')).hexdigest()
    return password_hash == stored_password

def perform_login(email, password):
    admin = User.query.filter_by(email=email, role='user').first()
    if hasattr(admin, "password"):
        password_verified = verify_password(admin.password, password, salt)
        if (password_verified == True):
            message = "login success"
            session['logged_in'] = True
            session['name'] = admin.first_name + " " + admin.last_name
        else:
            message = "login failed"
    else:
            message = "login failed"
   
    return message
