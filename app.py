import sys
from selenium import webdriver
import selenium.common.exceptions
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep # Can use sleep or selenium WebDriverWait
from instagram_login import username, password, has_2FA # Store your login info in this file
import os
from datetime import date

class InstaBot:
	"""Logs a user into  Instagram and finds their unfollowers"""
	def __init__(self, username, password, has_2FA):
		"""Logs into Instagram with login credentials from instagram_login"""
		if (len(username) < 1):
			print("Username must be at least 1 character")
			sys.exit()
		elif (len(password) < 6):
			print("Password must be at least 6 characters")
			sys.exit()
		self.username = username
		self.has_2FA = has_2FA
		# Set up the Selenium driver for Chrome
		self.driver = webdriver.Chrome(ChromeDriverManager().install())
		self.driver.get('http://www.instagram.com/')
		# Let the user see the page load
		sleep(3)

		try:
			print("Logging in")
			# Type the username and password into their fields,
			# then click the Log In button
			self.driver.find_element_by_name('username')\
				.send_keys(username)
			self.driver.find_element_by_name('password')\
				.send_keys(password)
			self.driver.find_element_by_xpath("//button[@type='submit']")\
				.click()
			if self.has_2FA:
				print("Complete your Two-factor authentication and click 'Confirm'")
				sleep(25)
			else:
				sleep(3)
			# Click the Not Now buttons for saving login and allowing notifications
			self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
				.click()
			sleep(1)
			self.driver.find_element_by_xpath("//button[contains(text(), 'Not Now')]")\
				.click()
		except Exception as exception:
			self.driver.quit()
			raise exception

	def get_unfollowers(self):
		"""Finds the Instagram user's unfollowers"""
		sleep(2)
		try:
			# Click on the username link then click on Followers
			self.driver.find_element_by_xpath("//a[contains(@href, '/{}')]".format(
				self.username)).click()
			sleep(3)
			self.driver.find_element_by_xpath("//a[contains(@href,'/followers')]")\
				.click()
		except Exception as exception:
			self.driver.quit()
			raise exception
		
		current_followers = self._get_usernames()
		self._compare_followers_with_old(current_followers)
		sleep(2)
		self.driver.quit()

	def _get_usernames(self):
		"""Scrolls down the Followers list and gets its usernames"""
		sleep(1)
		scroll_box = self.driver.find_element_by_xpath(
			'/html/body/div[5]/div/div/div[2]')
		print("Getting current followers")

		# Scroll down the Followers list until the end is reached
		prev_height, height = 0, 1
		# Compare the height of the box to the previous height before scrolling
		while prev_height != height:
			prev_height = height
			sleep(1)
			# Scroll to the bottom of the scroll box
			height = self.driver.execute_script("""
                arguments[0].scrollTo(0, arguments[0].scrollHeight); 
                return arguments[0].scrollHeight;
                """, scroll_box)
		# Get the usernames from the scroll box
		links = scroll_box.find_elements_by_tag_name('a')
		usernames = [username.text for username in links if username.text != '']
		# Click Close button
		self.driver.find_element_by_xpath(
			'/html/body/div[5]/div/div/div[1]/div/div[2]/button').click()
		return usernames

	def _compare_followers_with_old(self, current_followers):
		"""Compares current and old followers lists if an old list file exists"""
		if not os.path.exists('old_followers.txt'):
			# Create old followers file if it does not exist
			print(("No old followers file exists. "
				"Saving current followers to old_followers.txt"))
			with open('old_followers.txt', 'w') as filehandle:
				# Save current followers list line by line into the old list file
				for follower in current_followers:
					filehandle.write('%s\n' % follower)
				filehandle.close()
			print("Followers were successfully saved to old_followers.txt")
		else:
			print(("Old followers file exists. "
				"Comparing current followers to old ones from old_followers.txt"))
			old_followers = []
			# Open old followers file and read contents in as a list
			with open('old_followers.txt', 'r') as filehandle:
				for line in filehandle:
					# Remove linebreak which is the last character of the string
					follower = line[:-1]
					# Add follower to the list
					old_followers.append(follower)
				filehandle.close()
			
			with open('old_followers.txt', 'w') as filehandle:
				# Replace old followers list file with current followers
				for follower in current_followers:
					filehandle.write('%s\n' % follower)
				filehandle.close()
			print("old_followers.txt was updated to current followers")

			# Unfollowers are those in old_followers who are not in current_followers
			unfollowers = list(set(old_followers) - set(current_followers))
			if unfollowers:
				# Open history file of unfollowers and append any new unfollowers
				with open('unfollower_history.txt', 'a+') as filehandle:
					# Append today's date and the new unfollowers line by line
					# to the running history
					filehandle.write('%s\n' % date.today().strftime("%B %d, %Y"))
					for unfollower in unfollowers:
						filehandle.write('%s\n' % unfollower)
					filehandle.write('---------\n')
					filehandle.close()
				print(("New unfollowers were successfully found and saved to "
					"unfollower_history.txt"))
			else:
				print("No new unfollowers were found")


bot = InstaBot(username, password, has_2FA)
bot.get_unfollowers()
