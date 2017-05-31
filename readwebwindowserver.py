from selenium import webdriver

def initwebwindowsvr():
    driver = webdriver.PhantomJS('phantomjs')
    return driver
