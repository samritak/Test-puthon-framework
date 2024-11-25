# Flask = Framework para web service

# Dependencias de Flask
from flask import Flask, jsonify, request
# Selenium dependencies
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
# Dependencia sys para poder usar print
import sys


app = Flask(__name__)
driver = None
tabs = None

def validateDriver():
	global driver
	if ( driver is None ):
		return {'status': False, 'message': 'Driver not initialized'}
	try:
		title = driver.current_url
	except:
		return {'status': False, 'message': 'Disconnected Driver'}
	return {'status': True, 'message': 'Driver initiated'}

@app.route('/status', methods=['GET'])
def get_status():
	return jsonify(validateDriver())

@app.route('/init', methods=['GET'])
def get_init():
	global driver
	global tabs
	status = validateDriver();
	if ( status['status'] is False ):
		options = Options()
		# options.add_argument("--headless")
		# options.add_argument("--disable-gpu")
		# options.add_argument("--no-sandbox")
		# options.add_argument("--disable-infobars")
		# options.add_argument("--disable-dev-shm-usage")
		options.add_argument("enable-automation")
		driver = webdriver.Chrome(options=options)
		tabs = driver.window_handles
		return jsonify({'status': True, 'message': 'Initialized'})
	return jsonify({'status': True, 'message': 'Already Initiated'})

@app.route('/newtab', methods=['GET'])
def get_newtab():
	global driver
	global tabs
	status = validateDriver();
	if ( status['status'] is False ):
		return jsonify(status)
	driver.execute_script('''window.open("", "_blank");''');
	tabs = driver.window_handles
	return jsonify({'status': True, 'message': 'New Tab Opened'})

@app.route('/switchtab', methods=['GET'])
def get_switchtab():
	global driver
	global tabs
	status = validateDriver();
	tab = request.args.get('tab')
	if ( status['status'] is False ):
		return jsonify(status)
	if ( tab is not None ):
		ntab = int(tab) - 1;
		driver.switch_to_window(tabs[ntab])
		return jsonify({'status': True, 'message': 'Switched to tab: #' + tab})
	return jsonify({'status': False, 'message': 'No Tab No. provided, use ?tab=', 'tabs': tabs})

@app.route('/open', methods=['GET'])
def get_open():
	status = validateDriver()
	site = request.args.get('site')
	if ( site is None ):
		return jsonify({'status': False, 'message': 'Missing site parameter'})
	if ( status['status'] is True ):
		driver.get('http://' + site)
		return jsonify({'status': True})
	return jsonify(status)

@app.route('/close', methods=['GET'])
def get_close():
	global driver
	status = validateDriver()
	if ( status['status'] is True ):
		driver.close();
		driver = None;
		return jsonify({'status': True})
	return jsonify(status)

@app.route('/')
def index():
    return "Welcome"


if __name__ == '__main__':
    app.run(debug=True)