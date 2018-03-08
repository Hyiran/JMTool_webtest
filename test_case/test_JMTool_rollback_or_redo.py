# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re, sys, os
from page.TaskControlPageObject import TaskControlPage
from page.InspectionPageObject import InspectionPage
from page.LoginPage import LoginPage
from page.BusinessExecutionPageObject import BusinessExecutionPage
from common.Log import logger
from common.config import Config,CONFIG_FILE,LOG_PATH,REPORT_PATH,PAGE_PATH


class JMToolTaskControl(unittest.TestCase): 
    URL = Config().get('URL')
    #urly = Config().get('urlY')

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.URL) #外网测试环境
        self.driver.maximize_window() #窗口最大化
        LoginPage().login(self.driver,'admin','shuwei@123!') #调用登录函数登录 外网测试环境登录
        self.accept_next_alert = True

    '''以下部分为测试用例'''  
    def test_roll_back(self): #任务回滚
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行任务回滚用例*-*-*-*-*-'
        logger.info(testcase_title)
        driver.find_element_by_xpath("//ul[@id='collapse-nav9']/li[3]/a/span[2]").click() #点击任务管控链接 
        time.sleep(1)
        driver.find_element_by_xpath("(//button[@type='button'])[4]").click() #点击任务状态选择框
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='am-g']/div[3]/div/div/ul/li[2]/span").click() #选择待提交状态 
        time.sleep(2)
        task_id = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text #获取要操作的子任务id
        task_status = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text
        task_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").text
        task_list = [task_id,task_name,task_status]
        logger.info(task_list)
        driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[8]/div/button").click() #点击操作按钮
        time.sleep(1)
        driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[8]/div/ul/li[4]/a").click() #点击回滚按钮
        TaskControlPage().roll_back_remark(driver,'Autotest_rollback_successful!') #调用回滚备注框函数，输入内容
        driver.find_element_by_xpath("//div[@id='task-rollback']/div/div[3]/span[2]").click() #点击确定按钮
        time.sleep(3)
        self.assertEqual(u"完成回滚!", self.close_alert_and_get_its_text())
        time.sleep(1)
        TaskControlPage().business_execution_search_enter(driver,task_id) #调用业务执行-搜索输入框函数输入id
        driver.find_element_by_id("search_button").click() #点击搜索
        time.sleep(1)
        self.assertEqual(u"待领取",driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text) #比对任务状态是否为待领取，以判断是否回滚成功
        logger.info([task_id,task_name,driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text])
    
    
    def test_paid_task_redo(self): #完成（结算付款）-任务重做
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行完成（结算付款）-任务重做用例*-*-*-*-*-'
        logger.info(testcase_title)
        driver.find_element_by_xpath("//ul[@id='collapse-nav9']/li[3]/a/span[2]").click() #点击任务管控链接 
        driver.find_element_by_xpath("(//button[@type='button'])[4]").click() #点击任务状态选择框
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='am-g']/div[3]/div/div/ul/li[8]/span").click() #点击完成（结算付款）状态
        time.sleep(2)
        task_id = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text #获取要操作的子任务id
        task_status = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text
        task_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").text
        task_list = [task_id,task_name,task_status]
        logger.info(task_list)
        driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[8]/div/button").click() #点击操作按钮
        time.sleep(1)
        driver.find_element_by_link_text(u"重做").click() #点击重做按钮
        TaskControlPage().redo_remark(driver,'Autotest_paid_task_redo_successful!') #调用重做备注框函数，输入
        driver.find_element_by_xpath("//div[@id='task-again']/div/div[3]/span[2]").click()
        time.sleep(2)
        self.assertEqual(u"任务开始重做!",self.close_alert_and_get_its_text())
        TaskControlPage().business_execution_search_enter(driver,task_id)
        driver.find_element_by_id("search_button").click()
        time.sleep(1)
        self.assertEqual(u"待领取",driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text) #比对任务状态是否为待领取，以判断是否重做成功        
        logger.info([task_id,task_name,driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text])
    
    def test_no_paid_task_redo(self): #完成（无须付款）-任务重做
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行完成（无须付款）-任务重做用例*-*-*-*-*-'
        logger.info(testcase_title)
        driver.find_element_by_xpath("//ul[@id='collapse-nav9']/li[3]/a/span[2]").click() #点击任务管控链接 
        driver.find_element_by_xpath("(//button[@type='button'])[4]").click() #点击任务状态选择框
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='am-g']/div[3]/div/div/ul/li[9]/span").click() #点击完成（无须付款）状态
        time.sleep(2)
        task_id = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text
        task_status = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text
        task_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").text
        task_list = [task_id,task_name,task_status]
        logger.info(task_list)
        driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[8]/div/button").click() #点击操作按钮
        time.sleep(1)
        driver.find_element_by_link_text(u"重做").click() #点击重做按钮
        TaskControlPage().redo_remark(driver,'Autotest_no_paid_task_redo_successful!') #调用重做备注框函数，输入
        driver.find_element_by_xpath("//div[@id='task-again']/div/div[3]/span[2]").click()
        time.sleep(2)
        self.assertEqual(u"任务开始重做!",self.close_alert_and_get_its_text())
        TaskControlPage().business_execution_search_enter(driver,task_id)
        driver.find_element_by_id("search_button").click()
        time.sleep(1)
        self.assertEqual(u"待领取",driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text) #比对任务状态是否为待领取，以判断是否重做成功
        logger.info([task_id,task_name,driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text])


    def test_allocate_task(self): #任务分配
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行任务分配用例*-*-*-*-*-'
        logger.info(testcase_title)
        driver.find_element_by_xpath("//ul[@id='collapse-nav9']/li[3]/a/span[2]").click() #点击任务管控链接 
        driver.find_element_by_xpath("(//button[@type='button'])[4]").click() #点击任务状态选择框
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='am-g']/div[3]/div/div/ul/li[1]/span").click() #选择未领取状态 
        time.sleep(2)
        task_id = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text
        task_status = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text
        task_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").text
        task_list = [task_id,task_name,task_status]
        logger.info(task_list)
        time.sleep(1)
        driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[8]/div/button").click() #点击操作按钮
        time.sleep(1)
        driver.find_element_by_link_text(u"分配").click()  #点击分配按钮
        driver.find_element_by_id("search-text").click()
        driver.find_element_by_id("search-text").clear()
        driver.find_element_by_id("search-text").send_keys("马良")  #输入搜索条件
        driver.find_element_by_id("search-text").send_keys(Keys.ENTER)
        logger.info('输入内容：马良')
        driver.find_element_by_link_text(u"分配到用户").click() #点击分配到用户按钮
        driver.find_element_by_xpath("//div[@id='my-confirm']/div/div[3]/span[2]").click() #点击确定按钮
        time.sleep(2)
        self.assertEqual(u"任务分配成功", self.close_alert_and_get_its_text())
        BusinessExecutionPage().business_execution_menu(driver)
        BusinessExecutionPage().business_execution_search_enter(driver,task_id) #调用业务执行-搜索输入框函数输入id
        driver.find_element_by_id("search_button").click() #点击搜索
        time.sleep(1)
        self.assertEqual(u"马良",driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[8]/a").text)
        self.assertEqual(u"待提交",driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text)
        logger.info([task_id,task_name,driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[8]/a").text,driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text])

    def test_task_delete(self): #任务删除
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行任务删除用例*-*-*-*-*-'
        logger.info(testcase_title)
        driver.find_element_by_xpath("//ul[@id='collapse-nav9']/li[3]/a/span[2]").click() #点击任务管控链接
        time.sleep(1)
        driver.find_element_by_xpath("(//button[@type='button'])[4]").click() #点击任务状态选择框
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='am-g']/div[3]/div/div/ul/li[1]/span").click() #选择未领取状态 
        time.sleep(2)
        task_id = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text
        task_status = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text
        task_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").text
        task_list = [task_id,task_name,task_status]
        logger.info(task_list)
        driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[8]/div/button").click() #点击操作按钮
        time.sleep(1)
        driver.find_element_by_link_text(u"删除").click()  #点击删除按钮
        InspectionPage().delete_remark(driver,"Autotest_task_delete_successful!")
        logger.info('输入内容：Autotest_task_delete_successful!')
        time.sleep(1)
        driver.find_element_by_xpath("//div[@id='delete-confirm']/div/div[3]/span[2]").click() #点击确定按钮
        time.sleep(2)
        self.assertEqual(u"已完成!", self.close_alert_and_get_its_text())
        time.sleep(2)
        driver.find_element_by_id("getDeleteData").click() # 点击回收站
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='am-u-sm-12 am-u-md-2']/div/button").click() #点击选择搜索类型
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='am-u-sm-12 am-u-md-2']/div/div/ul/li[3]/span").click() #选择搜索类型为id
        time.sleep(1)
        BusinessExecutionPage().search_enter(driver,task_id)
        driver.find_element_by_id("search_button").click() #点击搜索
        time.sleep(2)
        self.assertEqual(task_id,driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text)
        self.assertEqual(u"已删除",driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[7]/span").text)
        logger.info([task_id,task_name,driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[7]/span").text])

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    testunit = unittest.TestSuite()
    testunit.addTest(JMToolInspection('test_roll_back'))
    testunit.addTest(JMToolInspection('test_paid_task_redo'))
    testunit.addTest(JMToolInspection('test_no_paid_task_redo'))
    testunit.addTest(JMToolInspection('test_allocate_task'))
    testunit.addTest(JMToolInspection('test_task_delete'))