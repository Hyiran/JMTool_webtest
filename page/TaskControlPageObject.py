import sys, unittest, time, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


class TaskControlPage:
    #精确搜索匹配ID，搜索框输入函数
    def business_execution_search_enter(self,driver,con_search):
        driver.find_element_by_xpath("//a[@id='clickHome']/span[2]").click() #点击业务执行链接
        time.sleep(1)
        driver.find_element_by_xpath("(//button[@type='button'])[12]").click() #点击选择匹配方式
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='am-u-sm-12 am-u-md-2 am-u-sm-offset-2']/div/div/ul/li[2]/span").click() #选择精确匹配
        driver.find_element_by_xpath("(//button[@type='button'])[13]").click() #点击选择搜索类型
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='am-u-sm-12 am-u-md-2']/div/div/ul/li[3]/span").click() #选择搜索类型为id
        driver.find_element_by_id("search-text").click()
        driver.find_element_by_id("search-text").clear()
        driver.find_element_by_id("search-text").send_keys(con_search)

	#回滚备注输入框函数
    def roll_back_remark(self,driver,con_roll_back_remark):
        driver.find_element_by_id("task-rollback-remark").click()
        driver.find_element_by_id("task-rollback-remark").clear()
        driver.find_element_by_id("task-rollback-remark").send_keys(con_roll_back_remark)
    #重做备注输入框函数
    def redo_remark(self,driver,con_redo_remark):
        driver.find_element_by_id("task-again-remark").click()
        driver.find_element_by_id("task-again-remark").clear()
        driver.find_element_by_id("task-again-remark").send_keys(con_redo_remark)