from flask import render_template, request, redirect, url_for, session
from admin.controllers import admin_controller

def list_users_view(page):
    if request.method == 'POST':
        name = request.form['name'].strip() if (request.form['name']) else ''
        email = request.form['email'].strip() if (request.form['email']) else ''
        phone = request.form['phone'].strip() if (request.form['phone']) else ''
        
        if (name or email or phone):
            users = admin_controller.search_users(name, email, phone, page)
            return render_template('admin/users.html', users=users)
        else:
            users = admin_controller.get_all_users(page)
            return render_template('admin/users.html', users=users)
    else:
        users = admin_controller.get_all_users(page)
        return render_template('admin/users.html', users=users)

def login_admin_view():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        message = admin_controller.perform_login( email, password)
        if (message == "login success"):
            return redirect(url_for('admin_bp.dashboard'))
        else:
            alert_message = "Incorrect username or password. Pease try again."
            return render_template('admin/login_form.html', alert_message=alert_message)
    else:
        if session.get('logged_in') is not None:
            return redirect(url_for('admin_bp.dashboard'))
        else:
            return render_template('admin/login_form.html')
