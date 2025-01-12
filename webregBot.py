import config
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# get user configuration
USERNAME_STR = config.CONFIG['USERNAME_STR']
PASSWORD_STR = config.CONFIG['PASSWORD_STR']
COURSES = config.CONFIG['COURSES']
SECTION_IDS = config.CONFIG['SECTION_IDS']
BROWSER = config.CONFIG['BROWSER']

if BROWSER == 'CHROME':
	browser = webdriver.Chrome('./driver/chromedriver')
elif BROWSER == 'PHANTOM':
	browser = webdriver.PhantomJS('./driver/phantomjs')
else:
	print 'Browser is not supported :('
	'''
	TODO
	write an exception if browser is not chrome or phantom 
	'''
browser.get(('https://act.ucsd.edu/webreg2'))

# enter username
username = browser.find_element_by_id('ssousername')
username.send_keys(USERNAME_STR)

# enter password
password = browser.find_element_by_id('ssopassword')
password.send_keys(PASSWORD_STR)

# click login
loginButton = browser.find_element_by_class_name('sso-button')
loginButton.click()

# select the intended quarter and click go
# -------------------------------------------
# uncomment these two lines below if the intended quarter is not the default one
# selectQuarter = Select(browser.find_element_by_id('startpage-select-term'))
# selectQuarter.select_by_visible_text('Summer Session II 2018')
# -------------------------------------------
goButton = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 'startpage-button-go')))
goButton.click()

# click on the textbox
for i in range(0, len(COURSES)):
	searchTextBox = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.ID, 's2id_autogen1')))
	searchTextBox.clear()
	searchTextBox.send_keys(COURSES[i])
	ignoreThis = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'select2-result-label')))
	ignoreThis.click()
	listClasses = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'ui-icon-circlesmall-plus')))
	listClasses.click()
	intendedSection = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '" + SECTION_IDS[i] + "')]")))
	enrollButton = intendedSection.find_element_by_xpath('..').find_element_by_class_name('search-enroll-class')
	if enrollButton.is_enabled():
		enrollButton.click()
		# check whether successful or not
		enrollAlert = WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.ID, 'dialog-enroll')))
		errorAlert = WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.CLASS_NAME, 'error')))
		if enrollAlert is not None:
			# click confirm
			confirmBtn = enrollAlert.find_element_by_xpath('..').find_element_by_class_name('ui-dialog-buttonset')
			confirmButton = WebDriverWait(confirmBtn, 10).until(EC.visibility_of_all_elements_located((By.XPATH, ".//*")))
			confirmButton[2].click()
			# close alert
			closeButton1 = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.ID, 'dialog-after-action-close')))
			closeButton1.click()
			print 'Successfully Enrolled in ' + COURSES[i]
		elif errorAlert is not None:
			print 'FAILED: Unable to Enroll in ' + COURSES[i]
			# close alert
			closeButton2 = WebDriverWait(browser, 10).until(EC.visibility_of_element_located((By.ID, 'dialog-after-action-close')))
			closeButton2.click()
	else:
		print 'FAILED: Already Enrolled in ' + COURSES[i]