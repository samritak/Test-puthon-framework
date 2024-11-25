from flask import jsonify, request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options


driver = None
tabs = None

def validateDriver():
	global driver
	if ( driver is None ):
		return {'status': False, 'message': 'Driver not initialized'}
	try:
		driver.current_url
	except:
		return {'status': False, 'message': 'Disconnected Driver'}
	return {'status': True, 'message': 'Driver initiated'}

def get_status():
	return jsonify(validateDriver())

def init():
	global driver
	global tabs
	status = validateDriver();
	if ( status['status'] is False ):
		# options = Options()
		# options.add_argument("--headless")
		# options.add_argument("--disable-gpu")
		# options.add_argument("--no-sandbox")
		# options.add_argument("--disable-infobars")
		# options.add_argument("--disable-dev-shm-usage")
		# options.add_argument("enable-automation")
		# driver = webdriver.Chrome(options=options)
		driver = webdriver.Chrome()
		driver.set_window_size(1024, 600)
		driver.maximize_window()
		tabs = driver.window_handles
		print({'status': True, 'message': 'Initialized'})
		return driver
	print({'status': True, 'message': 'Already Initialized'})
	return driver

def newtab():
	global driver
	global tabs
	status = validateDriver();
	if ( status['status'] is False ):
		return jsonify(status)
	driver.execute_script('''window.open("", "_blank");''');
	tabs = driver.window_handles
	return jsonify({'status': True, 'message': 'New Tab Opened'})

def switchtab():
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

def open(site):
	status = validateDriver()
	# site = request.args.get('site')
	if ( site is None ):
		return jsonify({'status': False, 'message': 'Missing site parameter'})
	if ( status['status'] is True ):
		driver.get('https://' + site)
		return driver
	return jsonify(status)

def close():
	global driver
	status = validateDriver()
	if ( status['status'] is True ):
		driver.close();
		driver = None;
		return jsonify({'status': True})
	return jsonify(status)
