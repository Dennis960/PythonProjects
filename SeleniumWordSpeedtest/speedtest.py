import time
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.remote.webelement import WebElement

driver = webdriver.Chrome(r'C:\Users\*******\Documents\chromedriver.exe')
driver.implicitly_wait(10)

driver.get('https://10fastfingers.com/typing-test/english')
inputField = driver.find_element_by_id('inputfield')
cookieButton = driver.find_element_by_id('CybotCookiebotDialogBodyLevelButtonLevelOptinDeclineAll')
driver.execute_script("arguments[0].click()", cookieButton)

wordsRoot = driver.find_element_by_id('row1')
html = wordsRoot.get_attribute('innerHTML')
soup = BeautifulSoup(str(html), 'html.parser')
for wordElement in soup.find_all('span'):
    word = wordElement.text
    inputField.send_keys(word + ' ')
