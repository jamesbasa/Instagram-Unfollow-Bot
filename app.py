import sys
from selenium import webdriver
from time import sleep
from instagram_login import username, password
import selenium.common.exceptions

class InstaBot:
	"""Logs a user in and finds their Instagram unfollowers"""
	def __init__(self, username, password):
		"""Logs into Instagram with login credentials from instagram_login"""
		if (len(username) < 1):
			print('Username must be at least 1 character')
			sys.exit()
		elif (len(password) < 6):
			print('Password must be at least 6 characters')
			sys.exit()
		self.username = username
		# Set up the Selenium driver for Chrome
		self.driver = webdriver.Chrome()
		self.driver.get('http://www.instagram.com/')
		# Let the user see the page load
		sleep(2)

		try:
			# Type the username and password into their fields,
			# then click the Log In button
			self.driver.find_element_by_name('username')\
				.send_keys(username)
			self.driver.find_element_by_name('password')\
				.send_keys(password)
			self.driver.find_element_by_xpath('//button[@type="submit"]')\
				.click()
		except Exception as exception:
			self.driver.quit()
			raise exception
		sleep(4)
		# Click the Not Now buttons for saving login and allowing notifications
		self.driver.find_element_by_xpath('//button[contains(text(), "Not Now")]')\
			.click()
		sleep(2)
		self.driver.find_element_by_xpath('//button[contains(text(), "Not Now")]')\
			.click()

		
bot = InstaBot(username, password)
