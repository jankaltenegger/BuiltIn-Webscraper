from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotVisibleException
from selenium.common.exceptions import ElementNotSelectableException
from selenium.common.exceptions import TimeoutException
from time import sleep
import csv

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
fluentwait = WebDriverWait(driver, timeout=10, poll_frequency=1, ignored_exceptions=[ElementNotVisibleException, ElementNotSelectableException, TimeoutException])

driver.get("https://builtin.com/companies/size/1-10-employees/11-50-employees/51-200-employees/201-500-employees/tech/google-cloud-companies?page=12")
sleep(10)
totalpage = int(driver.find_element(by=By.XPATH, value="//li[@class='page-item'][3]/a[@class='page-link']").text)
currentpage = int(driver.find_element(by=By.XPATH, value="//li[@class='page-item active']/a").text)
main = driver.current_window_handle

while currentpage < totalpage:
	i = 0
	while i < 20:
		fluentwait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-testid='company-column-"+str(i)+"']/section/h2/div/a")))
		driver.find_element(by=By.XPATH, value="//div[@data-testid='company-column-" + str(i) + "']/section/h2/div/a").click()
		fluentwait.until(EC.presence_of_element_located((By.XPATH, "//a[@class='info-item company-website-link']")))
		driver.find_element(by=By.XPATH, value="//a[@class='info-item company-website-link']").click()
		wait.until(EC.number_of_windows_to_be(2))

		for window_handle in driver.window_handles:
			if window_handle != main:
				driver.switch_to.window(window_handle)
				break
		with open('companyurls.csv', 'a', newline='') as f:
			thewriter = csv.writer(f)
			thewriter.writerow([driver.current_url])
		print(driver.current_url)
		driver.close()
		driver.switch_to.window(main)
		driver.back()
		i += 1
	fluentwait.until(EC.presence_of_element_located((By.XPATH, "//li[@class='page-next page-nav']/a")))
	driver.find_element(by=By.XPATH, value="//li[@class='page-next page-nav']/a").click()
	currentpage += 1
