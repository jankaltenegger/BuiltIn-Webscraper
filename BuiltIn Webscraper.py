from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import ElementNotSelectableException
from selenium.common.exceptions import TimeoutException
from time import sleep
import csv

# Declaration of variables used throughout the script
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
fluentwait = WebDriverWait(driver, timeout=10, poll_frequency=1, ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException, TimeoutException])


# Opens the chromedriver and navigates to the URL
driver.get("INSERT VALID URL HERE")
sleep(10)
# Gets the total amount of pages from an element
totalpage = int(driver.find_element(by=By.XPATH, value="//li[@class='page-item'][3]/a[@class='page-link']").text)
# Gets the current page from an element
currentpage = int(driver.find_element(by=By.XPATH, value="//li[@class='page-item active']/a").text)
main = driver.current_window_handle

# Loop for pages
while currentpage < totalpage:
	i = 0
	# Loop for companies within pages
	while i < 20:
		# Navigates to company page on builtin.com, figures out the URL of the company and opens it in a new tab
		fluentwait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid='company-column-"+str(i)+"']/section/h2/div/a")))
		driver.find_element(by=By.XPATH, value="//div[@data-testid='company-column-" + str(i) + "']/section/h2/div/a").click()
		fluentwait.until(EC.presence_of_element_located((By.XPATH, "//a[@class='info-item company-website-link']")))
		driver.find_element(by=By.XPATH, value="//a[@class='info-item company-website-link']").click()
		wait.until(EC.number_of_windows_to_be(2))

		# Navigates to new tab
		for window_handle in driver.window_handles:
			if window_handle != main:
				driver.switch_to.window(window_handle)
				break
		# Opens/creates a new .csv and writes down the current URL
		with open('companyurls.csv', 'a', newline='') as f:
			thewriter = csv.writer(f)
			thewriter.writerow([driver.current_url])
		driver.close()
		driver.switch_to.window(main)
		driver.back()
		i += 1
		
	# Flips to next page
	fluentwait.until(EC.presence_of_element_located((By.XPATH, "//li[@class='page-next page-nav']/a")))
	driver.find_element(by=By.XPATH, value="//li[@class='page-next page-nav']/a").click()
	currentpage += 1
