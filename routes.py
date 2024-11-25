from flask import Blueprint, render_template, session, redirect, url_for
from user.views.user_view import list_users_view, create_user_view, login_user_view, user_dashboard_view, user_aarp_tests_view
from user.controllers import user_controller
from user.tests.test_one import execute_test_one
from flask import Flask, request
import datetime,time
from config import Config
import glob, os,platform
from pyhtml2pdf import converter as pdf_convertor
from user.tests.CommonFunctions import TestCommonFunctions

 
user_bp = Blueprint("user_bp",
                    __name__,
                    template_folder="templates",
                    static_folder="static")


@user_bp.route("/")
def home():
    return redirect(url_for('user_bp.login'))

@user_bp.route('/list')
def users():
    return list_users_view()

@user_bp.route('/create', methods=['GET', 'POST'])
def create_user():
    return create_user_view()

@user_bp.route('/login',  methods=['GET', 'POST'])
def login():
    return login_user_view()

@user_bp.route('/logout')
def logout():
    session.pop('logged_in', None)
    # return login_user_view()
    return redirect(url_for('user_bp.login'))

@user_bp.route("/dashboard")
def dashboard():
    return user_dashboard_view()
    # return render_template("user/dashboard.html")

@user_bp.route("/aarp-tests")
def aarp_tests():
    return user_aarp_tests_view()

@user_bp.route("/test-one")
def test_one():
    retValue = execute_test_one()
    return retValue

@user_bp.route("/dashboard/aarp-dashboard", methods=["GET"])
def get_dashboard():
    print("Helloooooooooooo from get")
    return render_template('aarp.html')	
	
@user_bp.route('/aarp-dashboard-file', methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return "No file part in the request", 400
    file = request.files['file']
    print(file)
    if file.filename == '':
        return "No selected file", 400
    
    response = run_test_create_report('test_Aarp_Test_Suite', None, file)
    return response

@user_bp.route('/aarp-dashboard-url', methods=["POST"])
def upload():
    singleurl=request.form.get('singleurl')
    response = run_test_create_report('test_Aarp_Test_Suite',singleurl)
    return response

@user_bp.route('/test-Image-compare',methods=["POST"])
def upload_image():
    print("hello from image post upload")
    if 'file' not in request.files:
        return "No file part in the request", 400
    
    file = request.files['file']
    print(file)
    if file.filename == '':
        return "No selected file", 400
    #input_compare_type = 'Full page' #'Hero Section'
    singleurl=request.form.get('singleurl')
    input_compare_type=request.form.get('input_compare_type')
    print("=================================================hello from image post method\n\n")
    print("=============="+str(singleurl))
    print(input_compare_type)

    response = run_image_compare(file,singleurl,input_compare_type)
    print(response)
    print("Before returning from test image post upload")
    return response

# @user_bp.route("/dashboard/aarp-dashboard")
# def post_dashboard():
#     # Handle POST requests to the dashboard page
#     # You can process form data here
#     return render_template('dashboard.html')

def format_number(num):
    if num % 1 == 0:
        return int(num)
    else:
        return num
        
def update_input_csv(file):
    try:
        contents = file.read()
        with open(Config.CSV_FILE_PATH, 'wb') as f:
            f.write(contents)
        print("written in the input file")
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.close()

def get_report_file_name():
    date_time = datetime.datetime.now()
    unix_timestamp = format_number(time.mktime(date_time.timetuple()))
    report_file_name = str(unix_timestamp)
    return report_file_name

def get_response(report_file_name):
    return {"message": "Test executed successfully!",
            "Report": "/user/static/pdf/" + report_file_name,
            "file_name": report_file_name}

def delete_report_htmls():
    files = glob.glob(os.path.abspath('user/Reports/html/*.html'))
    for f in files:
        os.remove(f)

def generate_pdf_report(report_file_name):
    report_html_path = os.path.abspath("user/Reports/html/" + report_file_name + ".html")
    report_pdf_path = os.path.abspath("user/static/pdf/" + report_file_name + ".pdf")
    pdf_convertor.convert(f'file:///{report_html_path}', report_pdf_path)

# def delete_report_screenshots():
#     files = glob.glob(os.path.abspath('user/Reports/html/screenshot/*.png'))
#     for f in files:
#         os.remove(f)

def get_operating_system():
    return platform.system()

def run_test(singleurl,test_file_name):
    report_file_name = get_report_file_name()
    ops = get_operating_system()
    test_url = str(singleurl)
    print(test_url)

    if ops is not None and ops.lower() == 'linux':
        pytest_cmd = 'python3 -m pytest'
    else:
        pytest_cmd = 'python -m pytest'
    command = (pytest_cmd + ' user/tests/' + test_file_name + '.py --base-url="'+ test_url +'" --capture=sys -v --log-level=50 --html=user/Reports/html/' +
               report_file_name + '.html --css=user/static/css/aarpCheckList.css')
    os.system(command)

def run_test_create_report(test_file_name, singleurl=None, file='None'):
#def run_test_create_report(file, test_file_name):
    report_file_name = get_report_file_name()
    if file != 'None':
        update_input_csv(file)
    #delete_report_screenshots()
    run_test(singleurl,test_file_name)
    generate_pdf_report(report_file_name)
    #delete_report_htmls()
    response = get_response(report_file_name)
    return response

def get_image_response():
    return {
        "message": "Image UI Comparison executed successfully!",
        "Report1": "/static/pdf/"+"chrome_image_difference.pdf",
        "file_name1": "chrome_image_difference.pdf",
        "Report2": "/static/pdf/" + "chrome_image_grey_difference.pdf",
        "file_name2": "chrome_image_grey_difference.pdf",
        "Report3": "/static/pdf/" + "firefox_image_difference.pdf",
         "file_name3": "firefox_image_difference.pdf",
        "Report4": "/static/pdf/" + "firefox_image_grey_difference.pdf",
        "file_name4": "firefox_image_grey_difference.pdf"
    }

def upload_input_image(file):
    try:
        print("inside upload_input_image ")
        contents = file.read()
        with open(Config.IMAGE_FILE_PATH+'input_image.png', 'wb') as f:
            f.write(contents)
        print("file upload done !!")
    except Exception:
        return {"message": "There was an error uploading the image file"}
    finally:
        file.close()

def run_image_compare(file,url,input_compare_type):
    try:
        print("\n\nHello there 1 !!")
        common_functions = TestCommonFunctions()
        common_functions.remove_image_file()
        upload_input_image(file)
        print("\n\nHello there 2 !!")
        common_functions.run_image_comparison(url)
        time.sleep(2)
        print("\n\nHello there 3 !!")
        response = get_image_response()
        print("\n\nHello there 4!!")
        return response
        print("End of run_image_compare========================= ")
    except Exception as e:
        print("exception from run_image_compare compare " + str(e))