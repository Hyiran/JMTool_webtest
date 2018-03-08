# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re ,sys, os
from page.InspectionPageObject import InspectionPage
from page.BusinessExecutionPageObject import BusinessExecutionPage
from page.LoginPage import LoginPage
from common.Log import logger
from common.config import Config,CONFIG_FILE,LOG_PATH,REPORT_PATH,PAGE_PATH

class JMToolInspectionMain(unittest.TestCase):
    URL = Config().get('URL')

    # urly = Config().get('urlY')

    def setUp(self):  # 测试准备参数
        self.driver = webdriver.Chrome()
        self.driver.get(self.URL)  # 外网测试环境
        #self.driver.get(self.urly) #预发布环境
        self.driver.maximize_window()  # 窗口最大化
        LoginPage().login(self.driver, 'admin', 'shuwei@123!')  # 调用登录函数登录 外网测试环境登录
        #LoginPage().login(self.driver, 'admin', 'shuwei@12345!')  # 调用登录函数登录 预发布环境登录
        self.accept_next_alert = True

    def test_quality_inspection_not_pass(self):  #质检-任务质检页-质检不通过
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行质检-任务质检页-质检不通过用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        task_id = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text #获取要操作的子任务id
        task_status = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text
        task_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").text
        task_list = [task_id,task_name,task_status]
        logger.info(task_list)
        #获取当前标签句柄
        first_handle = driver.current_window_handle
        driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[14]/a/small").click() #点击操作-质检
        all_handles = driver.window_handles  # 获取所有窗口句柄
        for handle in all_handles:    #判断当前窗口句柄，切换窗口
            if handle != first_handle:
                driver.switch_to_window(handle)
        #切换窗口，进行质检操作
        driver.find_element_by_id("checkNoPass").click() #点击质检不通过按钮
        InspectionPage().inspection_not_pass_remark(driver,'Autotest_quality_inspection_not_pass!') #调用质检不通过备注框输入函数输入内容
        driver.find_element_by_css_selector("label.am-checkbox").click()
        driver.find_element_by_xpath("//div[@id='task-online-check']/div/div[4]/span[2]").click() #点击备注框确定按钮
        time.sleep(2)
        self.assertEqual(u"操作成功", self.close_alert_and_get_its_text())
        time.sleep(1)
        driver.switch_to_window(first_handle)        
        time.sleep(1)
        BusinessExecutionPage().business_execution_menu(driver)
        BusinessExecutionPage().business_execution_search_enter(driver,task_id) #调用业务执行-搜索输入框函数输入id
        driver.find_element_by_id("search_button").click() #点击搜索
        time.sleep(1)
        self.assertEqual(u"质检不通过",driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text) #比对任务状态是否为质检不通过，以判断是否质检不通过成功
        logger.info([task_id,task_name,driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text])

    def test_examine_and_approve_successful(self):  # 审批通过
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行审批通过用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        InspectionPage().switch_status_to_wait_to_approve(driver)
        task_id = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text  # 获取要操作的子任务id
        task_status = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text
        task_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").text
        task_list = [task_id, task_name, task_status]
        logger.info(task_list)
        driver.find_element_by_xpath("//table[@class='am-table am-table-bordered am-table-compact table-ms-size dataTable no-footer']/tbody/tr[1]/td[14]/div/button").click()  # 点击操作按钮
        time.sleep(1)
        driver.find_element_by_xpath("//table[@class='am-table am-table-bordered am-table-compact table-ms-size dataTable no-footer']/tbody/tr[1]/td[14]/div/ul/li[5]/a/small").click()  # 点击审批按钮
        driver.find_element_by_xpath("//div[@id='task-test-check-status-radios']/label[1]").click()  # 点击审批通过
        InspectionPage().approve_remark(driver, 'Autotest_successful!')  # 备注框输入内容
        driver.find_element_by_xpath("//div[@id='task-test-check']/div/div[3]/span[2]").click()  # 点击确定
        time.sleep(1)
        self.assertEqual(u"完成质检审批!", self.close_alert_and_get_its_text())
        BusinessExecutionPage().business_execution_menu(driver)
        BusinessExecutionPage().business_execution_search_enter(driver, task_id)  # 调用业务执行-搜索输入框函数输入id
        driver.find_element_by_id("search_button").click()  # 点击搜索
        time.sleep(1)
        self.assertEqual(u"待结算", driver.find_element_by_xpath(
            "//table[@id='dg']/tbody/tr/td[6]/span").text)  # 比对任务状态是否为待结算，以判断是否审批通过成功
        logger.info([task_id, task_name, driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text])

    def test_examine_and_approve_unsuccessful(self): #审批不通过
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行审批不通过用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        InspectionPage().switch_status_to_wait_to_approve(driver)
        task_id = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text #获取要操作的子任务id
        task_status = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text
        task_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").text
        task_list = [task_id, task_name, task_status]
        logger.info(task_list)
        driver.find_element_by_xpath("//table[@class='am-table am-table-bordered am-table-compact table-ms-size dataTable no-footer']/tbody/tr[1]/td[14]/div/button").click() #点击操作按钮
        time.sleep(1)
        driver.find_element_by_xpath("//table[@class='am-table am-table-bordered am-table-compact table-ms-size dataTable no-footer']/tbody/tr[1]/td[14]/div/ul/li[5]/a/small").click() #点击审批按钮  
        driver.find_element_by_xpath("//div[@id='task-test-check-status-radios']/label[2]").click() #点击不予通过
        InspectionPage().approve_remark(driver,'Autotest_unsuccessful!') #备注框输入内容-'自动化测试-'
        driver.find_element_by_xpath("//div[@id='task-test-check']/div/div[3]/span[2]").click() #点击确定
        time.sleep(1)      
        self.assertEqual(u"完成质检审批!", self.close_alert_and_get_its_text())
        BusinessExecutionPage().business_execution_menu(driver)
        BusinessExecutionPage().business_execution_search_enter(driver, task_id)  # 调用业务执行-搜索输入框函数输入id
        driver.find_element_by_id("search_button").click() #点击搜索
        time.sleep(1)
        self.assertEqual(u"审批不通过",driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text) #比对任务状态是否为审批不通过，以判断是否审批不通过成功
        logger.info([task_id, task_name, driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text])

    def test_settle_and_pay_money(self): #批量结算付款
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行批量结算付款用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        InspectionPage().switch_status_to_wait_to_settlement(driver)
        task_id = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text #获取要操作的子任务id
        task_status = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text
        task_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").text
        task_list = [task_id, task_name, task_status]
        logger.info(task_list)
        driver.find_element_by_xpath("//table[@id='dg']/tbody/tr[1]/td[15]/input").click() #选择勾选框 
        driver.find_element_by_link_text(u"批量结算（付款）").click() #点击批量结算付款
        time.sleep(1)
        self.assertEqual(u"完成结算质检!", self.close_alert_and_get_its_text())
        BusinessExecutionPage().business_execution_menu(driver)
        BusinessExecutionPage().business_execution_search_enter(driver, task_id)  # 调用业务执行-搜索输入框函数输入id
        driver.find_element_by_id("search_button").click() #点击搜索
        time.sleep(1)
        self.assertEqual(u"完成 (结算付款)",driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text) #比对任务状态是否为完成 (结算付款)，以判断是否结算成功
        logger.info([task_id, task_name, driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text])

    def test_settle_and_no_pay(self): #批量结算不付款
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行批量结算不付款用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        InspectionPage().switch_status_to_wait_to_settlement(driver)
        task_id = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text #获取要操作的子任务id
        task_status = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text
        task_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").text
        task_list = [task_id, task_name, task_status]
        logger.info(task_list)
        driver.find_element_by_xpath("//table[@id='dg']/tbody/tr[1]/td[15]/input").click() #选择勾选框 
        driver.find_element_by_link_text(u"批量结算（不付款）").click() #点击批量结算不付款
        time.sleep(1)     
        self.assertEqual(u"完成结算质检!", self.close_alert_and_get_its_text())
        BusinessExecutionPage().business_execution_menu(driver)
        BusinessExecutionPage().business_execution_search_enter(driver, task_id)  # 调用业务执行-搜索输入框函数输入id
        driver.find_element_by_id("search_button").click() #点击搜索
        time.sleep(1)
        self.assertEqual(u"完成 (无须付款)",driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text) #比对任务状态是否为完成 (无须付款)，以判断是否结算成功
        logger.info([task_id, task_name, driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text])

    def test_re_examine_successful(self): #质检不通过-复审通过
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行质检不通过-复审通过用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        InspectionPage().switch_status_to_quality_inspection_not_pass(driver)
        task_id = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text #获取要操作的子任务id
        task_status = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text
        task_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").text
        task_list = [task_id, task_name, task_status]
        logger.info(task_list)
        driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[14]/div/button").click() #点击操作按钮
        time.sleep(1)
        driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[14]/div/ul/li[5]/a/small").click() #点击复审(质检不通过)
        driver.find_element_by_xpath("//div[@id='task-online-check-nopass-review-status-radios']/label").click() #点击复审通过，回到待质检
        InspectionPage().re_examine_fail_remark(driver,'Autotest re-examine successful') #备注输入框输入内容
        driver.find_element_by_xpath("//div[@id='task-online-check-nopass-review']/div/div[3]/span[2]").click() #点击确定按钮
        time.sleep(2)
        self.assertEqual(u"完成质检不通过复审!", self.close_alert_and_get_its_text())
        BusinessExecutionPage().business_execution_menu(driver)
        BusinessExecutionPage().business_execution_search_enter(driver, task_id)  # 调用业务执行-搜索输入框函数输入id
        driver.find_element_by_id("search_button").click() #点击搜索
        time.sleep(1)
        self.assertEqual(u"待质检",driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text) #比对任务状态是否为待质检，以判断是否复审通过
        logger.info([task_id, task_name, driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text])

    def test_re_examine_unsuccessful(self): #质检不通过-复审不通过
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行质检不通过-复审不通过用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        InspectionPage().switch_status_to_quality_inspection_not_pass(driver)
        task_id = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text #获取要操作的子任务id
        task_status = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text
        task_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").text
        task_list = [task_id, task_name, task_status]
        logger.info(task_list)
        driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[14]/div/button").click() #点击操作按钮
        time.sleep(1)
        driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[14]/div/ul/li[5]/a/small").click() #点击复审(质检不通过)
        driver.find_element_by_xpath("//div[@id='task-online-check-nopass-review-status-radios']/label[2]").click() #点击不予通过，回到任务池
        InspectionPage().re_examine_fail_remark(driver,'Autotest re-examine unsuccessful')
        driver.find_element_by_xpath("//div[@id='task-online-check-nopass-review']/div/div[3]/span[2]").click() #点击确定按钮
        time.sleep(6)
        self.assertEqual(u"完成质检不通过复审!", self.close_alert_and_get_its_text())
        BusinessExecutionPage().business_execution_menu(driver)
        BusinessExecutionPage().business_execution_search_enter(driver, task_id)  # 调用业务执行-搜索输入框函数输入id
        driver.find_element_by_id("search_button").click() #点击搜索
        time.sleep(1)
        self.assertEqual(u"待领取",driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text) #比对任务状态是否为待领取，以判断是否复审不通过返回任务池成功
        logger.info([task_id, task_name, driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text])

    def test_reapprove_successful(self): #审批不通过-复审通过
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行审批不通过-复审通过用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        InspectionPage().switch_status_to_approve_not_pass(driver)
        task_id = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text #获取要操作的子任务id
        task_status = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text
        task_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").text
        task_list = [task_id, task_name, task_status]
        logger.info(task_list)
        driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[14]/div/button").click() #点击操作按钮
        time.sleep(1)
        driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[14]/div/ul/li[5]/a/small").click() #点击复审(审批不通过)
        driver.find_element_by_xpath("//div[@id='task-test-check-nopass-review-status-radios']/label").click() #点击复审通过，回到待审批
        InspectionPage().reapprove_remark(driver,'Autotest reapprove successful') #备注输入框输入内容
        driver.find_element_by_xpath("//div[@id='task-test-check-nopass-review']/div/div[3]/span[2]").click() #点击确定按钮
        time.sleep(6)
        self.assertEqual(u"完成审批不通过复审!", self.close_alert_and_get_its_text())
        BusinessExecutionPage().business_execution_menu(driver)
        BusinessExecutionPage().business_execution_search_enter(driver, task_id)  # 调用业务执行-搜索输入框函数输入id
        driver.find_element_by_id("search_button").click() #点击搜索
        time.sleep(1)
        self.assertEqual(u"待审批",driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text) #比对任务状态是否为待审批，以判断是否复审通过
        logger.info([task_id, task_name, driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text])

    def test_reapprove_unsuccessful(self): #审批不通过-不予通过
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行审批不通过-不予通过用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        InspectionPage().switch_status_to_approve_not_pass(driver)
        task_id = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text #获取要操作的子任务id
        task_status = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text
        task_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").text
        task_list = [task_id, task_name, task_status]
        logger.info(task_list)
        driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[14]/div/button").click() #点击操作按钮
        time.sleep(1)
        driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[14]/div/ul/li[5]/a/small").click() #点击复审(审批不通过)
        driver.find_element_by_xpath("//div[@id='task-test-check-nopass-review-status-radios']/label[2]").click() #点击不予通过，回到任务池
        InspectionPage().reapprove_remark(driver,'Autotest reapprove unsuccessful')
        driver.find_element_by_xpath("//div[@id='task-test-check-nopass-review']/div/div[3]/span[2]").click() #点击确定按钮
        time.sleep(6)
        self.assertEqual(u"完成审批不通过复审!", self.close_alert_and_get_its_text())
        BusinessExecutionPage().business_execution_menu(driver)
        BusinessExecutionPage().business_execution_search_enter(driver, task_id)  # 调用业务执行-搜索输入框函数输入id
        driver.find_element_by_id("search_button").click() #点击搜索
        time.sleep(1)
        self.assertEqual(u"待领取",driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text) #比对任务状态是否为待领取，以判断是否复审不通过返回任务池成功
        logger.info([task_id, task_name, driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[6]/span").text])

    def test_switch_scene(self):  #待质检状态-任务质检页-切换场景
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行待质检状态-任务质检页-切换场景用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        task_id = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text #获取要操作的子任务id
        task_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").text
        task_scene = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[3]").text
        logger.info([task_id,task_name,task_scene])
        InspectionPage().inspection_action(driver) #调用质检操作函数，点击操作按钮切换当前标签页
        driver.find_element_by_xpath("//button[@onclick='showMengban()']").click() #点击任务质检页-切换场景
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='change-mengban']/div/div/div[2]/ul/li[1]/button").click() #点击场景
        scene_goal = driver.find_element_by_xpath("//div[@class='change-mengban']/div/div/div[2]/ul/li[1]/button").text  #获取准备切换的场景
        driver.find_element_by_xpath("//button[@class='am-btn am-btn-success change-btn-cancel']").click()  #点击确认切换
        time.sleep(1)
        after_change_scene = driver.find_element_by_css_selector("#collectMsg > td:nth-child(3)").text #获取切换后的场景
        self.assertEqual(after_change_scene,scene_goal) #比对准备切换的场景和切换后的场景，一样则判断用例执行正确
        logger.info([task_id,task_name,after_change_scene])


    def test_switch_scene2(self): #待质检-采集点质检页-切换场景
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行待质检-采集点质检页-切换场景用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        task_id = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text #获取要操作的子任务id
        task_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").text
        task_scene = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[3]").text
        logger.info([task_id,task_name,task_scene])
        InspectionPage().inspection_action(driver) #调用质检操作函数，点击操作按钮切换当前标签页
        driver.find_element_by_id("norRetask").click() #点击无重复任务
        driver.find_element_by_id("confirmNext").click() #点击确认并下一步，切换至采集点质检页
        time.sleep(1)
        driver.find_element_by_xpath("//button[@onclick='showMengban()']").click() #点击切换场景
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='change-mengban']/div/div/div[2]/ul/li[1]/button").click() #点击场景
        scene_goal = driver.find_element_by_xpath("//div[@class='change-mengban']/div/div/div[2]/ul/li[1]/button").text  #获取准备切换的场景
        driver.find_element_by_xpath("//button[@class='am-btn am-btn-success change-btn-cancel']").click()  #点击确认切换
        time.sleep(1)
        self.assertEqual(u"不可用",driver.find_element_by_xpath("//div[@class='placeMsg']/a[1]").text)
        driver.find_element_by_id("taskCheck").click() #点击返回任务质检页
        time.sleep(1)
        after_change_scene = driver.find_element_by_css_selector("#collectMsg > td:nth-child(3)").text #获取切换后的场景
        self.assertEqual(after_change_scene,scene_goal) #比对准备切换的场景和切换后的场景，一样则判断用例执行正确
        logger.info([task_id,task_name,after_change_scene])

    def test_quality_inspection_not_pass_switch_scene(self): #质检不通过-任务质检页-切换场景
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行质检不通过-任务质检页-切换场景用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        InspectionPage().switch_status_to_quality_inspection_not_pass(driver)
        task_id = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text #获取要操作的子任务id
        task_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").text
        task_scene = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[3]").text
        logger.info([task_id,task_name,task_scene])
        InspectionPage().inspection_check_action(driver) #调用质检结果查看操作函数，点击操作按钮切换当前标签页
        driver.find_element_by_xpath("//button[@onclick='recoverBtn()']").click() #点击编辑按钮
        driver.find_element_by_xpath("//button[@onclick='showMengban()']").click() #点击任务质检页-切换场景
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='change-mengban']/div/div/div[2]/ul/li[1]/button").click() #点击场景
        scene_goal = driver.find_element_by_xpath("//div[@class='change-mengban']/div/div/div[2]/ul/li[1]/button").text  #获取准备切换的场景
        driver.find_element_by_xpath("//button[@class='am-btn am-btn-success change-btn-cancel']").click()  #点击确认切换
        time.sleep(1)
        after_change_scene = driver.find_element_by_css_selector("#collectMsg > td:nth-child(3)").text #获取切换后的场景
        self.assertEqual(after_change_scene,scene_goal) #比对准备切换的场景和切换后的场景，一样则判断用例执行正确
        logger.info([task_id,task_name,after_change_scene])

    def test_quality_inspection_not_pass_switch_scene2(self): #质检不通过-采集点质检页-切换场景
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行质检不通过-采集点质检页-切换场景用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        InspectionPage().switch_status_to_quality_inspection_not_pass(driver)
        task_id = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text #获取要操作的子任务id
        task_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").text
        task_scene = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[3]").text
        logger.info([task_id,task_name,task_scene])
        InspectionPage().inspection_check_action(driver) #调用质检结果查看操作函数，点击操作按钮切换当前标签页
        driver.find_element_by_xpath("//button[@onclick='recoverBtn()']").click() #点击编辑按钮
        driver.find_element_by_id("norRetask").click() #点击无重复任务
        driver.find_element_by_id("confirmNext").click() #点击确认并下一步，切换至采集点质检页
        time.sleep(1)
        driver.find_element_by_xpath("//button[@onclick='recoverBtn()']").click() #点击编辑按钮
        driver.find_element_by_xpath("//button[@onclick='showMengban()']").click() #点击任务质检页-切换场景
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='change-mengban']/div/div/div[2]/ul/li[1]/button").click() #点击场景
        scene_goal = driver.find_element_by_xpath("//div[@class='change-mengban']/div/div/div[2]/ul/li[1]/button").text  #获取准备切换的场景
        driver.find_element_by_xpath("//button[@class='am-btn am-btn-success change-btn-cancel']").click()  #点击确认切换
        time.sleep(1)
        self.assertEqual(u"不可用",driver.find_element_by_xpath("//div[@class='placeMsg']/a[1]").text)
        driver.find_element_by_id("taskCheck").click() #点击返回任务质检页
        time.sleep(1)
        after_change_scene = driver.find_element_by_css_selector("#collectMsg > td:nth-child(3)").text #获取切换后的场景
        self.assertEqual(after_change_scene,scene_goal) #比对准备切换的场景和切换后的场景，一样则判断用例执行正确
        logger.info([task_id,task_name,after_change_scene])


    def test_examine_and_approve_switch_scene(self): #待审批-任务质检页-切换场景
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行待审批-任务质检页-切换场景用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        InspectionPage().switch_status_to_wait_to_approve(driver)
        task_id = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text #获取要操作的子任务id
        task_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").text
        task_scene = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[3]").text
        logger.info([task_id,task_name,task_scene])
        InspectionPage().inspection_check_action(driver) #调用质检结果查看操作函数，点击操作按钮切换当前标签页
        driver.find_element_by_xpath("//button[@onclick='recoverBtn()']").click() #点击编辑按钮
        driver.find_element_by_xpath("//button[@onclick='showMengban()']").click() #点击任务质检页-切换场景
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='change-mengban']/div/div/div[2]/ul/li[1]/button").click() #点击场景
        scene_goal = driver.find_element_by_xpath("//div[@class='change-mengban']/div/div/div[2]/ul/li[1]/button").text  #获取准备切换的场景
        driver.find_element_by_xpath("//button[@class='am-btn am-btn-success change-btn-cancel']").click()  #点击确认切换
        time.sleep(1)
        after_change_scene = driver.find_element_by_css_selector("#collectMsg > td:nth-child(3)").text #获取切换后的场景
        self.assertEqual(after_change_scene,scene_goal) #比对准备切换的场景和切换后的场景，一样则判断用例执行正确
        logger.info([task_id,task_name,after_change_scene])

    def test_reapprove_switch_scene(self): #审批不通过-任务质检页-切换场景
        driver = self.driver
        testcase_title = '-*-*-*-*-*执行审批不通过-任务质检页-切换场景用例*-*-*-*-*-'
        logger.info(testcase_title)
        InspectionPage().quality_inspection_menu(driver)
        InspectionPage().switch_status_to_approve_not_pass(driver)
        task_id = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[1]").text #获取要操作的子任务id
        task_name = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[4]/a").text
        task_scene = driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[3]").text
        logger.info([task_id,task_name,task_scene])
        InspectionPage().inspection_check_action(driver) #调用质检结果查看操作函数，点击操作按钮切换当前标签页
        driver.find_element_by_xpath("//button[@onclick='recoverBtn()']").click() #点击编辑按钮
        driver.find_element_by_xpath("//button[@onclick='showMengban()']").click() #点击任务质检页-切换场景
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='change-mengban']/div/div/div[2]/ul/li[1]/button").click() #点击场景
        scene_goal = driver.find_element_by_xpath("//div[@class='change-mengban']/div/div/div[2]/ul/li[1]/button").text  #获取准备切换的场景
        driver.find_element_by_xpath("//button[@class='am-btn am-btn-success change-btn-cancel']").click()  #点击确认切换
        time.sleep(1)
        after_change_scene = driver.find_element_by_css_selector("#collectMsg > td:nth-child(3)").text #获取切换后的场景
        self.assertEqual(after_change_scene,scene_goal) #比对准备切换的场景和切换后的场景，一样则判断用例执行正确
        logger.info([task_id,task_name,after_change_scene])


    def is_element_present(self, how, what):
        try:
            self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: 
            return False
        return True

    def is_alert_present(self):
        try:
            self.driver.switch_to_alert()
        except NoAlertPresentException as e: 
            return False
        return True


    def close_alert_and_get_its_text(self): #判断弹框内容及比对、点击确定或取消
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                print (alert_text)
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self): #用例结束参数
        self.driver.quit() #关闭浏览器

    
if __name__ == "__main__":
    #unittest.main()
    testunit = unittest.TestSuite()
    testunit.addTest(JMToolInspection('test_quality_inspection_not_pass'))
    testunit.addTest(JMToolInspection('test_examine_and_approve_successful'))
    testunit.addTest(JMToolInspection('test_examine_and_approve_unsuccessful'))
    testunit.addTest(JMToolInspection('test_settle_and_pay_money'))
    testunit.addTest(JMToolInspection('test_settle_and_no_pay'))
    testunit.addTest(JMToolInspection('test_re_examine_successful'))
    testunit.addTest(JMToolInspection('test_re_examine_unsuccessful'))
    testunit.addTest(JMToolInspection('test_reapprove_successful'))
    testunit.addTest(JMToolInspection('test_reapprove_unsuccessful'))
    testunit.addTest(JMToolInspection('test_switch_scene'))
    testunit.addTest(JMToolInspection('test_switch_scene2'))
    testunit.addTest(JMToolInspection('test_quality_inspection_not_pass_switch_scene'))
    testunit.addTest(JMToolInspection('test_quality_inspection_not_pass_switch_scene2'))
    testunit.addTest(JMToolInspection('test_examine_and_approve_switch_scene'))
    testunit.addTest(JMToolInspection('test_reapprove_switch_scene'))
    