import time

from selenium import webdriver

# chromedriver.exe放到python.exe所在目录就不需要在下面Chrome()里写上路径了
driver =webdriver.Chrome()
driver.get('https://www.baidu.com/')
input_div=driver.find_element_by_id("kw").send_keys('python')
driver.find_element_by_xpath('//*[@id="su"]').click()

time.sleep(5) # delays for 5 seconds
driver.quit()
