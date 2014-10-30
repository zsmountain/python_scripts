'''
This program will automatically login to bing.com and search 30 times for PC search and 20 times for mobile search to get Bing credits.
Searching words are randomly read from a dictionary file. A standard Linux words file, usually stored at /usr/share/dict/words, or /usr/dict/words,
can be used.

This program is tested under Windows 7 64 bit platform.

More information about Bing rewards can be found at https://www.bing.com/explore/rewards

Requirements:
1. Python selenium module, which can be installed via pip
2. Chrome driver, which can be downloaded at http://chromedriver.storage.googleapis.com/index.html

Usage:
python bing_rewards.py EMAIL PASSWORD DICTFILE

'''

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
import time
import os
import random
import sys

if len(sys.argv) < 4:
	print('Usage:\npython ' + sys.argv[0] + ' EMAIL PASSWORD DICTFILE')
	sys.exit(1)

EMAIL = sys.argv[1]
PWD   = sys.argv[2]
DICT  = sys.argv[3]

with open(DICT) as f:
    DICT_COUNT = sum(1 for _ in f)

TIMEOUT_PAGE_LOAD = 10
HOME_PAGE = 'https://www.bing.com'
LOGIN_PAGE = 'https://login.live.com'

#PC Search
browser = webdriver.Chrome()
browser.get(LOGIN_PAGE)
browser.find_element_by_name('login').send_keys(EMAIL)
browser.find_element_by_name('passwd').send_keys(PWD)
browser.find_element_by_id('idSIButton9').click()
time.sleep(1)

if 'account.live.com' not in browser.current_url:
	print('Wrong username or password. Please correct and run again!')
	browser.close()
	sys.exit()

browser.get(HOME_PAGE)
WebDriverWait(browser, TIMEOUT_PAGE_LOAD).until(lambda x: x.find_element_by_id('sb_form_q'))
for i in range(30):
    rint = random.randint(1, DICT_COUNT)
    f = open(DICT,'r')
    for j, line in enumerate(f):
        if j == rint:
            browser.find_element_by_id('sb_form_q').send_keys(line)
            time.sleep(1)
            browser.find_element_by_id('sb_form_go').click()
            time.sleep(1)
            browser.find_element_by_id('sb_form_q').clear()
            time.sleep(1)
            break
    f.close()
browser.close()

#Mobile Search
options = webdriver.ChromeOptions()
options.add_argument('--user-agent=Mozilla/5.0 (iPhone; U; CPU iPhone OS 5_1_1 like Mac OS X; en) AppleWebKit/534.46.0 (KHTML, like Gecko) CriOS/19.0.1084.60 Mobile/9B206 Safari/7534.48.3')
browser = webdriver.Chrome(chrome_options=options)

browser.get(LOGIN_PAGE)
browser.find_element_by_name('login').send_keys(EMAIL)
browser.find_element_by_name('passwd').send_keys(PWD)
browser.find_element_by_id('idSIButton9').click()
time.sleep(1)


browser.get(HOME_PAGE)
WebDriverWait(browser, TIMEOUT_PAGE_LOAD).until(lambda x: x.find_element_by_id('sb_form_q'))
for i in range(20):
    rint = random.randint(1, DICT_COUNT)
    f = open(DICT,'r')
    for j, line in enumerate(f):
        if j == rint:
            browser.find_element_by_id('sb_form_q').send_keys(line)
            time.sleep(1)
            try:
                browser.find_element_by_id('sb_form_go').click()
            except:
                browser.find_element_by_id('sbBtn').click()
            time.sleep(1)
            browser.find_element_by_id('sb_form_q').clear()
            time.sleep(1)
            break
    f.close()
browser.close()
