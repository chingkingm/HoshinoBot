import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

if __name__ == '__main__':

    browser = webdriver.Chrome()
    
    browser.get('https://www.baidu.com')
    assert '百度一下' in browser.title

    elem = browser.find_element_by_id('kw')  # Find the search box
    elem.send_keys('selenium')
    browser.find_element_by_id('su').click()
    time.sleep(2)
    elem.clear()
    elem.send_keys('python办公自动化')
    browser.find_element_by_id('su').click()

    time.sleep(50000)
    browser.quit()
