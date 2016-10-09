# A plugin called firepath in firebox can inspect the element to give unique xpath. Hence, overall we can use that by_xpath to find
# element saving time from normally inspecting element. 
# Most importantly there are frames bounding in website. So if the frame is not switched to the one containing required element
# then code will give error with exception no such element found. Hence, be carefull about frame inculsion on website. For this,
# firepath can provide correct information alongside providing xpath.

from selenium import webdriver
import os

chromedriver="/home/shubh/python/chromedriver"
os.environ["webdriver.chrome.driver"]=chromedriver
browser=webdriver.Chrome(chromedriver)

browser.get("http://site24.way2sms.com/content/index.html")

mobEle=browser.find_element_by_xpath(".//*[@id='Login']/div[2]/form/div[1]/input")
mobEle.send_keys('9933988118')

passEle=browser.find_element_by_xpath(".//*[@id='Login']/div[2]/form/div[2]/input")
passEle.send_keys('blackhole')
passEle.submit()

smsEle=browser.find_element_by_xpath(".//*[@id='ebFrm']/div[2]/div[1]/input")
smsEle.click()

sendSMSEle=browser.find_element_by_xpath(".//*[@id='sendSMS']/a")
sendSMSEle.click()

browser.switch_to_frame('frame') ## iframe#frame is the ID of your iframe when looked from firepath

mobileEle=browser.find_element_by_xpath(".//*[@id='mobile']")
mobileEle.send_keys('9933988118')

messageEle=browser.find_element_by_xpath(".//*[@id='message']")
messageEle.send_keys('This is me, python !!! Pehchana ?')

SendEle=browser.find_element_by_id('Send')
SendEle.click()
