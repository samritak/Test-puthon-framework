import hashlib
from flask import jsonify, session
from models import db
from user.models.user import User
from config import Config

salt = Config.PASSWORD_HASH_SALT
per_page = 50

def hash_password(password, salt):
    password_hash = hashlib.sha256((password + salt).encode('utf-8')).hexdigest()
    return password_hash

def verify_password(stored_password, provided_password, salt):
    password_hash = hashlib.sha256((provided_password + salt).encode('utf-8')).hexdigest()
    return password_hash == stored_password

def perform_login(email, password):
    admin = User.query.filter_by(email=email, role='admin').first()
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

def get_all_users(page):
    users = User.query.filter_by(role='user').paginate(page=page, per_page=per_page, error_out=False)
    return users

def search_users(name, email, phone, page):
    filter = "" # , role='user'
    per_page=10

    if (name):
        search = "%{}%".format(name)
        filter = User.first_name.like(search)
        filter += User.last_name.like(search)
    elif (email):
        search = "%{}%".format(email)
        filter = User.email.like(search)
    elif (phone):
        search = "%{}%".format(phone)
        filter = User.phone.like(search)
    
    users = User.query.filter(filter).paginate(page=page, per_page=per_page, error_out=False)
    return users
