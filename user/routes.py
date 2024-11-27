from flask import Blueprint, render_template, session, request, redirect, url_for
from user.views.user_view import (
    list_users_view,
    create_user_view,
    login_user_view,
    user_dashboard_view,
    user_aarp_tests_view,
    display_aarp_test_view,
    user_inogen_tests_view,
    user_jaya_tests_view,
    user_rif_tests_view,
    user_greeting_genie_tests_view,
)
from user.tests.common_functions import TestCommonFunctions

user_bp = Blueprint(
    "user_bp", __name__, template_folder="templates", static_folder="static"
)


@user_bp.route("/")
def home():
    return redirect(url_for("user_bp.login"))


def substring_after(s, delim):
    return s.partition(delim)[1]


@user_bp.route("/list")
def users():
    return list_users_view()


@user_bp.route("/create", methods=["GET", "POST"])
def create_user():
    return create_user_view()


@user_bp.route("/login", methods=["GET", "POST"])
def login():
    return login_user_view()


@user_bp.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("user_bp.login"))


@user_bp.route("/dashboard")
def dashboard():
    return user_dashboard_view()


@user_bp.route("/aarp-tests")
def aarp_tests():
    return user_aarp_tests_view()


@user_bp.route("/inogen-tests")
def inogen_tests():
    return user_inogen_tests_view()


@user_bp.route("/rif-tests")
def rif_tests():
    return user_rif_tests_view()


@user_bp.route("/jaya-tests")
def jaya_tests():
    return user_jaya_tests_view()


@user_bp.route("/greeting-genie-tests")
def greeting_genie_tests():
    return user_greeting_genie_tests_view()


@user_bp.route("/test-image-compare", methods=["POST"])
def upload_image():
    return TestCommonFunctions.run_image_compare(request)


@user_bp.route("/dashboard/aarp-dashboard", methods=["GET"])
def get_dashboard():
    return render_template("aarp.html")


@user_bp.route("/aarp-tests/<page_path>", methods=["GET", "POST"])
def display_run_aarp_tests(page_path):
    print("Page Path: " + page_path)
    print("Req Method: " + request.method)
    test_names = request.form.get('test_names')
    print("Reqest test names: ")
    print(test_names)
    if request.method.upper() == "GET":
        test_names = request.args.get('test_names')
        print(test_names)
        test_title = page_path.replace("-", " ").replace("aarp", "").strip().title()
        return display_aarp_test_view("aarp-test", page_path, test_title, test_names)
    elif request.method.upper() == "POST":
        if page_path.endswith("-file"):
            test_file = "test_" + page_path.replace("-file", "")
            test_file = test_file.replace("-", "_")
            return TestCommonFunctions.run_test_with_file(test_file, test_names)
        elif page_path.endswith("-url"):
            test_file = "test_" + page_path.replace("-url", "")
            test_file = test_file.replace("-", "_")
            return TestCommonFunctions.run_test_with_url(test_file, test_names)
