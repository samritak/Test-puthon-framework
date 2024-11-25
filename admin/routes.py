from flask import Blueprint, render_template, session, redirect, url_for, request
from admin.views.admin_view import list_users_view, login_admin_view
 
admin_bp = Blueprint("admin_bp",
                     __name__,
                     template_folder="templates",
                     static_folder="static")

@admin_bp.route("/")
def home():
    return render_template("admin/index.html")

@admin_bp.route('/user-list',  methods=['GET', 'POST'])
def users():
    page = int(request.args.get('page')) if(request.args.get('page')) else 1
    return list_users_view(page)

# @admin_bp.route('/user-list/<int:page>',  methods=['GET'])
# def list_users():
#     page = request.args.get('page') if(request.args.get('page')) else 1
#     return list_users_view(page)

@admin_bp.route('/login',  methods=['GET', 'POST'])
def login():
    return login_admin_view()

@admin_bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    # return login_user_view()
    return redirect(url_for('admin_bp.login'))

@admin_bp.route("/dashboard")
def dashboard():
    return render_template("admin/dashboard.html")