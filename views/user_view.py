from flask import render_template, request, redirect, url_for, session
from user.controllers import user_controller

def list_users_view():
    users = user_controller.get_all_users()
    return render_template('user/users.html', users=users)

def create_user_view():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        password = request.form['password']
        user_controller.create_user(first_name, last_name, email, phone, password)
        return redirect(url_for('user_bp.users'))
    return render_template('user/create_user_form.html')

def login_user_view():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        message = user_controller.perform_login( email, password)
        if (message == "login success"):
            return redirect(url_for('user_bp.dashboard'))
            # return render_template('user/dashboard.html')
        else:
            alert_message = "Incorrect username or password. Pease try again."
            return render_template('user/login_form.html', alert_message=alert_message)
    else:
        if session.get('logged_in') is not None:
            # return render_template('user/dashboard.html')
            return redirect(url_for('user_bp.dashboard'))
        else:
            return render_template('user/login_form.html')

def user_dashboard_view():
    if session.get('logged_in') is not None:
         return render_template('user/dashboard.html')
    else:
        return redirect(url_for('user_bp.login'))

def user_aarp_tests_view():
    if session.get('logged_in') is not None:
         return render_template('user/aarp.html')
    else:
        return redirect(url_for('user_bp.login'))
