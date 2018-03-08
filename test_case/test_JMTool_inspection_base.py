# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re, sys,os
from page.InspectionPageObject import InspectionPage
from page.BusinessExecutionPageObject import BusinessExecutionPage
from page.LoginPage import LoginPage
from common.Log import logger
from common.config import Config,CONFIG_FILE,LOG_PATH,REPORT_PATH,PAGE_PATH

class JMToolInspectionBase(unittest.TestCase):
    URL = Config().get('URL')

    # urly = Config().get('urlY')

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(self.URL)  # 外网测试环境
        #self.driver.get(self.urly) #预发布环境
        self.driver.maximize_window()  # 窗口最大化
        LoginPage().login(self.driver, 'admin', 'shuwei@123!')  # 调用登录函数登录 外网测试环境登录
        #LoginPage().login(self.driver, 'admin', 'shuwei@12345!')  # 调用登录函数登录 预发布环境登录
        self.accept_next_alert = True
    
    def test_quality_inspection_city_search(self):  #质检-按城市搜索
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行质检-按城市搜索用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        driver.find_element_by_xpath("(//button[@type='button'])[2]").click() #点击所在城市选择框
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='am-u-sm-12 am-u-md-3']/div/div/ul/li/span").click() #点选深圳市
        logger.info('选择搜索条件：'+ driver.find_element_by_xpath("//div[@class='am-u-sm-12 am-u-md-3']/div/div/ul/li/span").text)
        time.sleep(1)
        city_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[2]").text
        self.assertIn(u"深圳市",city_name)
        self.assertEqual(u"待质检",driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text)
        logger.info([city_name,driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text])

    def test_quality_inspection_area_search(self):  #质检-按区域搜索
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行质检-按区域搜索用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        driver.find_element_by_xpath("(//button[@type='button'])[2]").click() #点击所在城市选择框
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='am-u-sm-12 am-u-md-3']/div/div/ul/li/span").click() #点选深圳市
        logger.info('选择搜索条件：'+ driver.find_element_by_xpath("//div[@class='am-u-sm-12 am-u-md-3']/div/div/ul/li/span").text)
        driver.find_element_by_xpath("(//button[@type='button'])[3]").click() #点击所在区域选择框
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[4]/span").click() #点选南山区
        logger.info('选择搜索条件：'+ driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[4]/span").text)
        time.sleep(1)
        area_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[2]").text
        self.assertIn(u"南山区",area_name)
        self.assertEqual(u"待质检",driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text)
        logger.info([area_name,driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text])

    def test_quality_inspection_scene_type_search(self):  #质检-按场景类型搜索
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行质检-按场景类型搜索用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        driver.find_element_by_xpath("(//button[@type='button'])[4]").click() #点击场景类型选择框
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='am-g']/div[3]/div/div/ul/li").click() #点选商场场景
        logger.info('选择搜索条件：'+ driver.find_element_by_xpath("//div[@class='am-g']/div[3]/div/div/ul/li").text)
        time.sleep(1)
        self.assertEqual(u"商场",driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[3]").text)
        self.assertEqual(u"待质检",driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text)
        logger.info([driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[3]").text,driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text])

    def test_quality_inspection_task_source_search(self):  #质检-按任务来源-采集员-搜索
        driver = self.driver        
        testcase_title = '-*-*-*-*-*执行质检-按任务来源-采集员-搜索用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        driver.find_element_by_xpath("(//button[@type='button'])[5]").click() #点击任务来源选择框
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='am-g']/div[4]/div/div/ul/li[3]/span").click() #选择采集员
        logger.info('选择搜索条件：' + driver.find_element_by_xpath("//div[@class='am-g']/div[4]/div/div/ul/li[3]/span").text) 
        time.sleep(1)
        self.assertEqual(u"采集员",driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/span").text)
        self.assertEqual(u"待质检",driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text)
        logger.info([driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/span").text,driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text])

    def test_quality_inspection_task_source_search2(self):  #质检-按任务来源-官方-搜索
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行质检-按任务来源-官方-搜索用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        driver.find_element_by_xpath("(//button[@type='button'])[5]").click() #点击任务来源选择框
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='am-g']/div[4]/div/div/ul/li[2]/span").click() #选择官方
        logger.info('选择搜索条件：' + driver.find_element_by_xpath("//div[@class='am-g']/div[4]/div/div/ul/li[2]/span").text)
        time.sleep(1)
        self.assertEqual(u"",driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/span").text)
        self.assertEqual(u"待质检",driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text)
        logger.info([driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/span").text,driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text])

    def test_task_status_to_be_get_search(self):  #质检-按任务状态-未领取-搜索
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行质检-按任务状态-未领取-搜索用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        driver.find_element_by_xpath("(//button[@type='button'])[6]").click() #点击任务状态下拉框
        driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[3]/span").click() #取消选择'待质检'
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[1]/span").click() #点击选择'未领取'
        logger.info('选择搜索条件：' + driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[1]/span").text)
        time.sleep(3)
        task_id = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text #获取要操作的子任务id
        task_status = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text
        task_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").text
        task_list = [task_id,task_name,task_status]
        self.assertEqual(u"待领取",task_status)
        logger.info(task_list)

    def test_task_status_to_be_submit_search(self):  #质检-按任务状态-待提交-搜索
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行质检-按任务状态-待提交-搜索用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        driver.find_element_by_xpath("(//button[@type='button'])[6]").click() #点击任务状态下拉框
        driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[3]/span").click() #取消选择'待质检'
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[2]/span").click() #点击选择'待提交'
        logger.info('选择搜索条件：' + driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[2]/span").text)
        time.sleep(3)
        task_id = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text #获取要操作的子任务id
        task_status = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text
        task_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").text
        task_list = [task_id,task_name,task_status]
        self.assertEqual(u"待提交",task_status)
        logger.info(task_list)

    def test_task_status_quality_inspection_not_pass_search(self):  #质检-按任务状态-质检不通过-搜索
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行质检-按任务状态-质检不通过-搜索用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        driver.find_element_by_xpath("(//button[@type='button'])[6]").click() #点击任务状态下拉框
        driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[3]/span").click() #取消选择'待质检'
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[4]/span").click() #点击选择'质检不通过'
        logger.info('选择搜索条件：' + driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[4]/span").text)
        time.sleep(3)
        task_id = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text #获取要操作的子任务id
        task_status = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text
        task_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").text
        task_list = [task_id,task_name,task_status]
        self.assertEqual(u"质检不通过",task_status)
        logger.info(task_list)

    def test_task_status_pend_to_approve_search(self):  #质检-按任务状态-待审批-搜索
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行质检-按任务状态-待审批-搜索用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        driver.find_element_by_xpath("(//button[@type='button'])[6]").click() #点击任务状态下拉框
        driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[3]/span").click() #取消选择'待质检'
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[5]/span").click() #点击选择'待审批'
        logger.info('选择搜索条件：' + driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[5]/span").text)
        time.sleep(3)
        task_id = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text #获取要操作的子任务id
        task_status = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text
        task_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").text
        task_list = [task_id,task_name,task_status]
        self.assertEqual(u"待审批",task_status)
        logger.info(task_list)

    def test_task_status_approve_not_pass_search(self):  #质检-按任务状态-审批不通过-搜索
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行质检-按任务状态-待审批-搜索用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        driver.find_element_by_xpath("(//button[@type='button'])[6]").click() #点击任务状态下拉框
        driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[3]/span").click() #取消选择'待质检'
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[6]/span").click() #点击选择'审批不通过'
        logger.info('选择搜索条件：' + driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[6]/span").text)
        time.sleep(3)
        task_id = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text #获取要操作的子任务id
        task_status = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text
        task_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").text
        task_list = [task_id,task_name,task_status]
        self.assertEqual(u"审批不通过",task_status)
        logger.info(task_list)

    def test_task_status_to_be_settled_search(self):  #质检-按任务状态-待结算-搜索
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行质检-按任务状态-待结算-搜索用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        driver.find_element_by_xpath("(//button[@type='button'])[6]").click() #点击任务状态下拉框
        driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[3]/span").click() #取消选择'待质检'
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[7]/span").click() #点击选择'待结算'
        logger.info('选择搜索条件：' + driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[7]/span").text)
        time.sleep(3)
        task_id = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text #获取要操作的子任务id
        task_status = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text
        task_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").text
        task_list = [task_id,task_name,task_status]
        self.assertEqual(u"待结算",task_status)
        logger.info(task_list)

    def test_task_status_settle_and_pay_money_search(self):  #质检-按任务状态-完成 (结算付款)-搜索
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行质检-按任务状态-完成 (结算付款)-搜索用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        driver.find_element_by_xpath("(//button[@type='button'])[6]").click() #点击任务状态下拉框
        driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[3]/span").click() #取消选择'待质检'
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[8]/span").click() #点击选择'完成 (结算付款)'
        logger.info('选择搜索条件：' + driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[8]/span").text)
        time.sleep(3)
        task_id = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text #获取要操作的子任务id
        task_status = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text
        task_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").text
        task_list = [task_id,task_name,task_status]
        self.assertEqual(u"完成 (结算付款)",task_status)
        logger.info(task_list)

    def test_task_status_settle_and_no_pay_search(self):  #质检-按任务状态-完成 (无须付款)-搜索
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行质检-按任务状态-完成 (结算付款)-搜索用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        driver.find_element_by_xpath("(//button[@type='button'])[6]").click() #点击任务状态下拉框
        driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[3]/span").click() #取消选择'待质检'
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[9]/span").click() #点击选择'完成 (无须付款)'
        logger.info('选择搜索条件：' + driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[9]/span").text)
        time.sleep(3)
        task_id = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text #获取要操作的子任务id
        task_status = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text
        task_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").text
        task_list = [task_id,task_name,task_status]
        self.assertEqual(u"完成 (无须付款)",task_status)
        logger.info(task_list)

    def test_check_status_search(self):  #质检-按检测状态-已检测-搜索
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行质检-按检测状态-已检测-搜索用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        driver.find_element_by_xpath("(//button[@type='button'])[7]").click() #点击检测状态下拉框
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='am-g am-margin-top-sm']/div[2]/div/div/ul/li[2]/span").click() #点击选择已检测
        logger.info('选择搜索条件：' + driver.find_element_by_xpath("//div[@class='am-g am-margin-top-sm']/div[2]/div/div/ul/li[2]/span").text)
        time.sleep(1)
        task_id = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text #获取要操作的子任务id
        task_status = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text
        task_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").text
        point = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[13]/a[1]").text
        photo = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[13]/a[2]").text
        signal = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[13]/a[3]").text
        check_mark = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[13]/a[4]").text
        self.assertEqual(u"已检测",check_mark) 
        logger.info([task_id,task_name,task_status,point,photo,signal,check_mark])

    def test_check_status_search2(self):  #质检-按检测状态-未检测-搜索
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行质检-按检测状态-未检测-搜索用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        driver.find_element_by_xpath("(//button[@type='button'])[7]").click() #点击检测状态下拉框
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='am-g am-margin-top-sm']/div[2]/div/div/ul/li[3]/span").click() #点击选择未检测
        logger.info('选择搜索条件：' + driver.find_element_by_xpath("//div[@class='am-g am-margin-top-sm']/div[2]/div/div/ul/li[3]/span").text)
        time.sleep(1)
        task_id = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text #获取要操作的子任务id
        task_status = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text
        task_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").text
        point = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[13]/a[1]").text
        photo = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[13]/a[2]").text
        signal = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[13]/a[3]").text
        #check_mark = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[13]/a[4]").text
        list_check_status = [point,photo,signal]
        self.assertNotIn(u"",list_check_status) #比对结果不存在list里
        logger.info([task_id,task_name,task_status,point,photo,signal])

    def test_belong_to_team_search(self):  #质检-按所属团队-搜索
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行质检-按所属团队-搜索用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        driver.find_element_by_xpath("(//button[@type='button'])[8]").click() #点击所属团队下拉框
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='am-g am-margin-top-sm']/div[3]/div/div/ul/li[97]/span").click() #点击选择奋斗
        logger.info('选择搜索条件：' + driver.find_element_by_xpath("//div[@class='am-g am-margin-top-sm']/div[3]/div/div/ul/li[97]/span").text)
        time.sleep(1)
        task_id = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text #获取要操作的子任务id
        task_status = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text
        task_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").text
        task_team = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[7]").text
        self.assertEqual(u"奋斗",task_team)
        logger.info([task_id,task_name,task_status,task_team])

    def test_phonenumber_search(self): #质检-模糊匹配-按手机号-搜索
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行质检-按手机号-搜索用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        driver.find_element_by_xpath("(//button[@type='button'])[12]").click() #点击选择搜索类型 
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='admin-content-body']/div[7]/div[5]/div/div/ul/li/span").click() #选择搜索类型为任务名 
        logger.info('选择搜索条件：' + driver.find_element_by_xpath("//div[@class='admin-content-body']/div[7]/div[5]/div/div/ul/li/span").text)
        InspectionPage().search_enter(driver,'134')
        time.sleep(1)
        logger.info('输入内容：134')
        driver.find_element_by_id("search_button").click()
        time.sleep(1)
        task_id = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text #获取要操作的子任务id
        task_status = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text
        task_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").text
        time.sleep(1)
        #获取当前标签句柄
        first_handle = driver.current_window_handle
        driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[8]/a[1]").click() #点击采集员姓名链接
        all_handles = driver.window_handles  # 获取所有窗口句柄
        for handle in all_handles:    #判断当前窗口句柄，切换窗口
            if handle != first_handle:
                driver.switch_to_window(handle) 
        phonenum = driver.find_element_by_xpath("//div[@class='am-g']/div/form/fieldset/div[3]/div/input").get_attribute("value") #获取手机号码
        self.assertIn(u"134",phonenum)
        logger.info([task_id,task_name,task_status,phonenum])

    def test_task_name_search(self): #质检-模糊匹配-按任务名-搜索
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行质检-按任务名-搜索用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        logger.info('选择搜索条件：' + driver.find_element_by_xpath("//div[@class='admin-content-body']/div[7]/div[5]/div/div/ul/li[2]/span").text)
        InspectionPage().search_enter(driver,'水')
        time.sleep(1)
        logger.info('输入内容：水')
        driver.find_element_by_id("search_button").click()
        time.sleep(1)
        task_id = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text #获取要操作的子任务id
        task_status = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text
        task_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").text
        self.assertIn(u"水",task_name)
        logger.info([task_id,task_name,task_status])

    def test_task_id_search(self): #质检-模糊匹配-按id-搜索
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行质检-按id-搜索用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        driver.find_element_by_xpath("(//button[@type='button'])[12]").click() #点击选择搜索类型 
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='admin-content-body']/div[7]/div[5]/div/div/ul/li[3]/span").click() #选择搜索类型为id
        logger.info('选择搜索条件：' + driver.find_element_by_xpath("//div[@class='admin-content-body']/div[7]/div[5]/div/div/ul/li[3]/span").text)
        InspectionPage().search_enter(driver,'123')
        logger.info('输入内容：123')
        driver.find_element_by_id("search_button").click()
        time.sleep(1)
        task_id = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text #获取要操作的子任务id
        task_status = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text
        task_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").text
        self.assertIn(u"123",driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text)
        logger.info([task_id,task_name,task_status])

    def test_task_username_search(self): #质检-模糊匹配-按采集员-搜索
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行质检-按采集员-搜索用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        driver.find_element_by_xpath("(//button[@type='button'])[12]").click() #点击选择搜索类型 
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='admin-content-body']/div[7]/div[5]/div/div/ul/li[4]/span").click() #选择搜索类型为采集员
        logger.info('选择搜索条件：' + driver.find_element_by_xpath("//div[@class='admin-content-body']/div[7]/div[5]/div/div/ul/li[4]/span").text)
        InspectionPage().search_enter(driver,'李')
        logger.info('输入内容：李')
        driver.find_element_by_id("search_button").click()
        time.sleep(1)
        task_id = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text #获取要操作的子任务id
        task_status = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text
        task_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").text
        user_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[8]/a[1]").text
        self.assertIn(u"李",user_name)
        logger.info([task_id,task_name,task_status,user_name])

    def test_phonenumber_accurate_search(self): #质检-精确匹配-按手机号-搜索
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行质检-精确匹配-按手机号-搜索用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        InspectionPage().inspection_page_accurate_search(driver)
        driver.find_element_by_xpath("//div[@class='admin-content-body']/div[7]/div[5]/div/div/ul/li[1]/span").click() #选择搜索类型为手机号
        logger.info('选择匹配方式：精确匹配，选择搜索条件：'+ driver.find_element_by_xpath("//div[@class='admin-content-body']/div[7]/div[5]/div/div/ul/li[1]/span").text)
        time.sleep(1)
        InspectionPage().search_enter(driver,'13570863628')
        logger.info('输入内容：13570863628')
        driver.find_element_by_id("search_button").click()
        time.sleep(1)
        task_id = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text #获取要操作的子任务id
        task_status = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text
        task_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").text
        #获取当前标签句柄
        first_handle = driver.current_window_handle
        driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[8]/a[1]").click() #点击采集员姓名链接
        all_handles = driver.window_handles  # 获取所有窗口句柄
        for handle in all_handles:    #判断当前窗口句柄，切换窗口
            if handle != first_handle:
                driver.switch_to_window(handle) 
        phonenum = driver.find_element_by_xpath("//div[@class='am-g']/div/form/fieldset/div[3]/div/input").get_attribute("value") #获取手机号码
        self.assertEqual(u"13570863628",phonenum)
        logger.info([task_id,task_status,task_name,phonenum])

    def test_task_name_accurate_search(self): #质检-精确匹配-按任务名-搜索
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行质检-精确匹配-按任务名-搜索用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        InspectionPage().inspection_page_accurate_search(driver)
        task_id = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text #获取要操作的子任务id
        task_status = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text
        task_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").text #获取当前页面第一个任务名
        driver.find_element_by_xpath("//div[@class='admin-content-body']/div[7]/div[5]/div/div/ul/li[2]/span").click() #选择搜索类型为任务名 
        logger.info('选择匹配方式：精确匹配，选择搜索条件：'+ driver.find_element_by_xpath("//div[@class='admin-content-body']/div[7]/div[5]/div/div/ul/li[2]/span").text)
        time.sleep(1)
        InspectionPage().search_enter(driver,task_name)
        logger.info('输入内容：'+task_name)
        driver.find_element_by_id("search_button").click()
        time.sleep(1)
        self.assertEqual(task_name,driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a[1]").text)
        logger.info([task_id,task_status,driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a[1]").text])

    def test_task_id_accurate_search(self): #质检-精确匹配-按id-搜索
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行质检-精确匹配-按id-搜索用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        InspectionPage().inspection_page_accurate_search(driver)
        task_id = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text
        task_status = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text
        task_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").text #获取当前页面第一个任务名
        driver.find_element_by_xpath("//div[@class='admin-content-body']/div[7]/div[5]/div/div/ul/li[3]/span").click() #选择搜索类型为id
        logger.info('选择匹配方式：精确匹配，选择搜索条件：'+ driver.find_element_by_xpath("//div[@class='admin-content-body']/div[7]/div[5]/div/div/ul/li[3]/span").text)
        time.sleep(1)
        InspectionPage().search_enter(driver,task_id)
        logger.info('输入内容：'+task_id)
        driver.find_element_by_id("search_button").click()
        time.sleep(1)
        self.assertEqual(task_id,driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text)
        logger.info([driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text,task_status,task_name])

    def test_task_username_accurate_search(self): #质检-精确匹配-按采集员-搜索
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行质检-精确匹配-按采集员-搜索用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        InspectionPage().inspection_page_accurate_search(driver)
        driver.find_element_by_xpath("//div[@class='admin-content-body']/div[7]/div[5]/div/div/ul/li[4]/span").click() #选择搜索类型为采集员
        logger.info('选择匹配方式：精确匹配，选择搜索条件：'+ driver.find_element_by_xpath("//div[@class='admin-content-body']/div[7]/div[5]/div/div/ul/li[4]/span").text)
        InspectionPage().search_enter(driver,'马良')
        logger.info('输入内容：马良')
        driver.find_element_by_id("search_button").click()
        time.sleep(1)
        task_id = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text
        task_status = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text
        task_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").text #获取当前页面第一个任务名
        user_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[8]/a[1]").text
        self.assertEqual(u"马良",user_name)
        logger.info([task_id,task_status,task_name,user_name])

    def test_point_link(self): #质检-检测状态-采集点
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行质检-检测状态-采集点用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        task_id = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text
        task_status = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text
        task_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").text #获取当前页面第一个任务名
        string = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[13]/a[1]").text
        point_num = re.findall(r"\d+\.?\d*",string)[0] #获取点数量
        #获取当前标签句柄
        first_handle = driver.current_window_handle
        driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[13]/a[1]").click() #点击 点连接，进入采集点详情页
        all_handles = driver.window_handles  # 获取所有窗口句柄
        for handle in all_handles:    #判断当前窗口句柄，切换窗口
            if handle != first_handle:
                driver.switch_to_window(handle)
        page_point_sum = re.findall(r"\d+\.?\d*", driver.find_element_by_xpath("//div[@class='am-u-sm-12']/div/div/div[2]/div").text) #获取采集点详情页点总数
        self.assertIn(point_num,page_point_sum)
        logger.info([task_id,task_status,task_name,string,point_num,page_point_sum])


    def test_signal_link(self): #质检-检测状态-信号
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行质检-检测状态-信号用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        task_id = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text
        task_status = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text
        task_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").text #获取当前页面第一个任务名
        string = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[13]/a[3]").text
        signal_num = re.findall(r"\d+\.?\d*",string)[0] #获取信号数量
        #获取当前标签句柄
        first_handle = driver.current_window_handle
        driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[13]/a[3]").click() #点击 信号连接，进入采集点信号详情页
        all_handles = driver.window_handles  # 获取所有窗口句柄
        for handle in all_handles:    #判断当前窗口句柄，切换窗口
            if handle != first_handle:
                driver.switch_to_window(handle)
        page_signal_sum = re.findall(r"\d+\.?\d*", driver.find_element_by_xpath("//div[@class='am-u-sm-12']/div/div/div[2]/div").text) #获取采集点信号详情页信号总数
        self.assertIn(signal_num,page_signal_sum)
        logger.info([task_id,task_status,task_name,string,signal_num,page_signal_sum])


    def test_operational_point_details(self):  #质检-操作-采集点详情
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行质检-操作-采集点详情用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[14]/div/button").click() #点击操作按钮
        time.sleep(1)
        task_id = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text
        task_status = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text
        task_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").text #获取当前页面第一个任务名
        point_details_num = re.findall(r"\d+\.?\d*",driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[14]/div/ul/li/a/small").text)[0] #获取采集点详情按钮中的数字
        #获取当前标签句柄
        first_handle = driver.current_window_handle
        driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[14]/div/ul/li/a").click() #点击采集点详情
        all_handles = driver.window_handles  # 获取所有窗口句柄
        for handle in all_handles:    #判断当前窗口句柄，切换窗口
            if handle != first_handle:
                driver.switch_to_window(handle)
        page_sum = re.findall(r"\d+\.?\d*", driver.find_element_by_xpath("//div[@class='am-u-sm-12']/div/div/div[2]/div").text) #获取采集点详情页点总数
        self.assertIn(point_details_num,page_sum)
        logger.info([task_id,task_status,task_name,point_details_num,page_sum])


    def test_operational_delete_submit(self): #质检-操作-删除-确定
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行质检-操作-删除-确定用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        task_id = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text
        driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[14]/div/button").click() #点击操作按钮
        time.sleep(1)
        driver.find_element_by_link_text(u"删除").click()
        logger.info('点击删除按钮')
        InspectionPage().delete_remark(driver,'Autotest_delete_successful!')
        logger.info('输入内容：Autotest_delete_successful')
        time.sleep(1)
        driver.find_element_by_xpath("//div[@id='delete-confirm']/div/div[3]/span[2]").click() #点击确定按钮
        logger.info('点击确定按钮')
        time.sleep(1)
        self.assertEqual(u"已完成!", self.close_alert_and_get_its_text())
        driver.find_element_by_link_text(u"采集任务").click()  #点击采集任务链接
        time.sleep(1)
        driver.find_element_by_xpath("//ul[@id='collapse-nav9']/li[3]/a/span[2]").click() #点击任务管控
        driver.find_element_by_id("getDeleteData").click() #点击回收站按钮
        driver.find_element_by_xpath("html/body/div[2]/div[2]/div/div[4]/div[1]/div[3]/div/button").click()  #点击搜索类型  /html/body/div[2]/div[2]/div/div[4]/div[1]/div[3]/div/button
        time.sleep(1)
        driver.find_element_by_xpath("html/body/div[2]/div[2]/div/div[4]/div[1]/div[3]/div/div/ul/li[3]").click() #点选id
        logger.info('选择搜索类型：'+ driver.find_element_by_xpath("html/body/div[2]/div[2]/div/div[4]/div[1]/div[3]/div/div/ul/li[3]").text)
        time.sleep(1)
        InspectionPage().search_enter(driver,task_id)
        logger.info('输入内容：'+task_id)
        driver.find_element_by_id("search_button").click()
        time.sleep(1)
        self.assertEqual(task_id,driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text)
        self.assertEqual(u"已删除",driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[7]/span").text)
        logger.info([driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text,driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[3]").text,
            driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").text,driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[7]/span").text])


    def test_operational_delete_cancel(self): #质检-操作-删除-取消
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行质检-操作-删除-取消用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[14]/div/button").click() #点击操作按钮
        time.sleep(1)
        driver.find_element_by_link_text(u"删除").click()
        logger.info('点击删除按钮')
        InspectionPage().delete_remark(driver,'Autotest_delete_cancel!')
        logger.info('输入内容：Autotest_delete_cancel')
        time.sleep(1)
        driver.find_element_by_xpath("//div[@id='delete-confirm']/div/div[3]/span[1]").click() #点击取消按钮
        logger.info('点击取消按钮')
        time.sleep(1)
        self.assertEqual(u"待质检",driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text)

    def test_task_name_link(self): #质检-点击任务名链接
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行质检-点击任务名链接用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        task_id = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text
        task_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").text #获取子任务名称
        task_city = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[2]").text #获取子任务城市区域
        task_scene = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[3]").text #获取任务场景
        task_street = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[5]").text #获取任务街道
        task_team = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[7]").text #获取采集员团队
        task_user = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[8]/a[1]").text #获取采集员手机号
        time.sleep(1)
        #获取当前标签句柄
        first_handle = driver.current_window_handle
        driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").click() #点击任务名称
        all_handles = driver.window_handles  # 获取所有窗口句柄
        for handle in all_handles:    #判断当前窗口句柄，切换窗口
            if handle != first_handle:
                driver.switch_to_window(handle)
        self.assertEqual(task_name,driver.find_element_by_xpath("//form[@class='am-form am-form-horizontal']/fieldset/div/div/div/input").get_attribute("value"))
        self.assertEqual(task_scene,driver.find_element_by_xpath("//form[@class='am-form am-form-horizontal']/fieldset[2]/div/div/div/input").get_attribute("value"))
        self.assertEqual(task_street,driver.find_element_by_xpath("//form[@class='am-form am-form-horizontal']/fieldset[2]/div[2]/div/input").get_attribute("value"))
        self.assertEqual(task_user,driver.find_element_by_xpath("//form[@class='am-form am-form-horizontal']/fieldset[2]/div[7]/div/input").get_attribute("value"))
        self.assertEqual(task_team,driver.find_element_by_xpath("//form[@class='am-form am-form-horizontal']/fieldset[2]/div[7]/div[2]/input").get_attribute("value"))
        self.assertIn(driver.find_element_by_xpath("//form[@class='am-form am-form-horizontal']/fieldset[2]/div/div/div[2]/div/input").get_attribute("value"),task_city)
        self.assertIn(driver.find_element_by_xpath("//form[@class='am-form am-form-horizontal']/fieldset[2]/div/div/div[3]/div/input").get_attribute("value"),task_city)
        logger.info(['任务id：'+task_id,'任务名称：'+driver.find_element_by_xpath("//form[@class='am-form am-form-horizontal']/fieldset/div/div/div/input").get_attribute("value"),
            '场景：'+driver.find_element_by_xpath("//form[@class='am-form am-form-horizontal']/fieldset[2]/div/div/div/input").get_attribute("value"),
            '街道：'+driver.find_element_by_xpath("//form[@class='am-form am-form-horizontal']/fieldset[2]/div[2]/div/input").get_attribute("value"),
            '采集员：'+driver.find_element_by_xpath("//form[@class='am-form am-form-horizontal']/fieldset[2]/div[7]/div/input").get_attribute("value"),
            '所属团队：'+driver.find_element_by_xpath("//form[@class='am-form am-form-horizontal']/fieldset[2]/div[7]/div[2]/input").get_attribute("value"),
            '城市：'+driver.find_element_by_xpath("//form[@class='am-form am-form-horizontal']/fieldset[2]/div/div/div[2]/div/input").get_attribute("value"),
            '区域：'+driver.find_element_by_xpath("//form[@class='am-form am-form-horizontal']/fieldset[2]/div/div/div[3]/div/input").get_attribute("value")])


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
    testunit.addTest(JMToolInspection('test_quality_inspection_city_search'))
    testunit.addTest(JMToolInspection('test_quality_inspection_area_search'))
    testunit.addTest(JMToolInspection('test_quality_inspection_scene_type_search'))
    testunit.addTest(JMToolInspection('test_quality_inspection_task_source_search'))
    testunit.addTest(JMToolInspection('test_quality_inspection_task_source_search2'))
    testunit.addTest(JMToolInspection('test_task_status_to_be_get_search'))
    testunit.addTest(JMToolInspection('test_task_status_to_be_submit_search'))
    testunit.addTest(JMToolInspection('test_task_status_quality_inspection_not_pass_search'))
    testunit.addTest(JMToolInspection('test_task_status_pend_to_approve_search'))
    testunit.addTest(JMToolInspection('test_task_status_approve_not_pass_search'))
    testunit.addTest(JMToolInspection('test_task_status_to_be_settled_search'))
    testunit.addTest(JMToolInspection('test_task_status_settle_and_pay_money_search'))
    testunit.addTest(JMToolInspection('test_task_status_settle_and_no_pay_search'))
    testunit.addTest(JMToolInspection('test_check_status_search'))
    testunit.addTest(JMToolInspection('test_check_status_search2'))
    testunit.addTest(JMToolInspection('test_belong_to_team_search'))
    testunit.addTest(JMToolInspection('test_phonenumber_search'))
    testunit.addTest(JMToolInspection('test_task_name_search'))
    testunit.addTest(JMToolInspection('test_task_id_search'))
    testunit.addTest(JMToolInspection('test_task_username_search'))
    testunit.addTest(JMToolInspection('test_phonenumber_accurate_search'))
    testunit.addTest(JMToolInspection('test_task_name_accurate_search'))
    testunit.addTest(JMToolInspection('test_task_id_accurate_search'))
    testunit.addTest(JMToolInspection('test_task_username_accurate_search'))
    testunit.addTest(JMToolInspection('test_point_link'))
    testunit.addTest(JMToolInspection('test_signal_link'))
    testunit.addTest(JMToolInspection('test_operational_point_details'))
    testunit.addTest(JMToolInspection('test_operational_delete_submit'))
    testunit.addTest(JMToolInspection('test_operational_delete_cancel'))
    testunit.addTest(JMToolInspection('test_task_name_link'))