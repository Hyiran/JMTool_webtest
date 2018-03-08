import sys, unittest, time, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

class LoginPage:
    #登录函数
    def login(self,driver,user,pw):
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys(user)
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys(pw)
        driver.find_element_by_id("password").send_keys(Keys.ENTER)