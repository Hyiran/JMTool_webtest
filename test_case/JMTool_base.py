# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
from HTMLTestRunner import HTMLTestRunner
import unittest, time, re 

class JMToolTestCase(unittest.TestCase): #JMTool测试类
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://pre-release.jmtool.papakaka.com:81/JMTool/admin/login.jhtml") #默认打开url  预发布环境
        #self.driver.get("http://stbi-test.jjfinder.com:81/JMTool/admin/login.jhtml") #外网测试环境
        self.driver.maximize_window() #窗口最大化
        self.login('admin','shuwei@12345!') #调用登录函数登录 预发布环境登录
        #self.login('admin','shuwei@123!') #调用登录函数登录 外网测试环境登录
        self.accept_next_alert = True
    '''常用函数'''
    #登录函数
    def login(self,user,pw):
        self.driver.find_element_by_id("username").clear()
        self.driver.find_element_by_id("username").send_keys(user)
        self.driver.find_element_by_id("password").clear()
        self.driver.find_element_by_id("password").send_keys(pw)
        self.driver.find_element_by_id("password").send_keys(Keys.ENTER)
    #审批-备注框输入函数
    def approve_remark(self,con_approve_remark): 
        self.driver.find_element_by_id("task-test-check-remark").click()
        self.driver.find_element_by_id("task-test-check-remark").clear()
        self.driver.find_element_by_id("task-test-check-remark").send_keys(con_approve_remark)
    #点击质检菜单函数
    def quality_inspection_menu(self):
        self.driver.find_element_by_xpath("//div[@id='admin-offcanvas']/div/ul/li[5]/a/span[2]").click() #点击任务质检菜单
        time.sleep(1)
        self.driver.find_element_by_xpath("//ul[@id='collapse-nav10']/li/a/span[2]").click() #点击质检菜单
        time.sleep(1)
    #复审不通过-备注框输入函数
    def re_examine_fail_remark(self,con_re_examine_fail_remark):
        self.driver.find_element_by_id("task-online-check-nopass-review-remark").click()
        self.driver.find_element_by_id("task-online-check-nopass-review-remark").clear()
        self.driver.find_element_by_id("task-online-check-nopass-review-remark").send_keys(con_re_examine_fail_remark)
    #审批不通过-备注框输入函数
    def reapprove_remark(self,con_reapprove_remark):
        self.driver.find_element_by_id("task-test-check-nopass-review-remark").click()
        self.driver.find_element_by_id("task-test-check-nopass-review-remark").clear()
        self.driver.find_element_by_id("task-test-check-nopass-review-remark").send_keys(con_reapprove_remark)

    '''以下部分为测试用例'''
    def atest_quality_inspection_successful_and_no_pay(self):  #质检-可用不付款
        driver = self.driver
        self.quality_inspection_menu()
        #获取当前标签句柄
        first_handle = driver.current_window_handle
        driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[14]/a/small").click() #点击操作-质检
        all_handles = driver.window_handles  # 获取所有窗口句柄
        for handle in all_handles:    #判断当前窗口句柄，切换窗口
            if handle != first_handle:
                print ('swich to new_handle')  # 输出待选择的窗口句柄
                driver.switch_to_window(handle)
        #切换窗口，进行质检操作
        driver.find_element_by_id("norRetask").click() #点击无重复任务
        driver.find_element_by_id("confirmNext").click() #点击确认下一步
        driver.find_element_by_link_text(u"可用").click() #点击可用
        #driver.find_element_by_xpath(u"(//a[contains(text(),'可用')])[5]").click()
        driver.find_element_by_id("isUsabled").click() #点击是否可用
        driver.find_element_by_xpath("//div[@id='checkUseble']/label[2]").click() #点击可用不付款
        driver.find_element_by_id("toSure").click()
        time.sleep(2) #固定等待2s
        #self.imgname = time.strftime("%Y_%m_%d_%H_%M_%S") + '_quality_inspection_successful_and_no_pay.png'       
        self.assertEqual(u"操作成功", self.close_alert_and_get_its_text())

    def atest_examine_and_approve_successful(self): #审批通过
        driver = self.driver
        self.quality_inspection_menu()
        driver.find_element_by_xpath("(//button[@type='button'])[6]").click() #点击任务状态下拉框
        driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[3]/span").click() #取消选择'待质检'
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[5]/span").click() #点击选择'待审批'
        time.sleep(3)
        driver.find_element_by_xpath("//table[@class='am-table am-table-bordered am-table-compact table-ms-size dataTable no-footer']/tbody/tr[1]/td[14]/div/button").click() #点击操作按钮
        time.sleep(1)
        driver.find_element_by_xpath("//table[@class='am-table am-table-bordered am-table-compact table-ms-size dataTable no-footer']/tbody/tr[1]/td[14]/div/ul/li[5]/a/small").click() #点击审批按钮   
        time.sleep(1)
        driver.find_element_by_xpath("//div[@id='task-test-check-status-radios']/label[1]").click() #点击审批通过
        self.approve_remark('Autotest_successful!') #备注框输入内容
        driver.find_element_by_xpath("//div[@id='task-test-check']/div/div[3]/span[2]").click() #点击确定
        time.sleep(1)
        #self.imgname = time.strftime("%Y_%m_%d_%H_%M_%S") + '_examine_and_approve_successful.png'        
        self.assertEqual(u"完成质检审批!", self.close_alert_and_get_its_text())

    def atest_examine_and_approve_unsuccessful(self): #审批不通过
        driver = self.driver
        self.quality_inspection_menu()
        driver.find_element_by_xpath("(//button[@type='button'])[6]").click() #点击任务状态下拉框
        driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[3]/span").click() #取消选择'待质检'
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[5]/span").click() #点击选择'待审批'
        time.sleep(3)
        driver.find_element_by_xpath("//table[@class='am-table am-table-bordered am-table-compact table-ms-size dataTable no-footer']/tbody/tr[1]/td[14]/div/button").click() #点击操作按钮
        time.sleep(1)
        driver.find_element_by_xpath("//table[@class='am-table am-table-bordered am-table-compact table-ms-size dataTable no-footer']/tbody/tr[1]/td[14]/div/ul/li[5]/a/small").click() #点击审批按钮   
        time.sleep(1)
        driver.find_element_by_xpath("//div[@id='task-test-check-status-radios']/label[2]").click() #点击不予通过
        self.approve_remark('Autotest_unsuccessful!') #备注框输入内容-'自动化测试-'
        driver.find_element_by_xpath("//div[@id='task-test-check']/div/div[3]/span[2]").click() #点击确定
        time.sleep(1)
        #self.imgname = time.strftime("%Y_%m_%d_%H_%M_%S") + '_examine_and_approve_unsuccessful.png'        
        self.assertEqual(u"完成质检审批!", self.close_alert_and_get_its_text())

    def atest_settle_and_pay_money(self): #批量结算付款
        driver = self.driver
        self.quality_inspection_menu()
        driver.find_element_by_xpath("(//button[@type='button'])[6]").click() #点击任务状态下拉框
        driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[3]/span").click() #取消选择'待质检'
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[7]/span").click() #选择待结算
        time.sleep(3)
        driver.find_element_by_xpath("//table[@id='dg']/tbody/tr[1]/td[15]/input").click() #选择勾选框 
        driver.find_element_by_link_text(u"批量结算（付款）").click() #点击批量结算付款
        time.sleep(2)        
        #self.imgname = time.strftime("%Y_%m_%d_%H_%M_%S") + '_settle_and_pay_money.png'
        self.assertEqual(u"完成结算质检!", self.close_alert_and_get_its_text())

    def atest_settle_and_no_pay(self): #批量结算不付款
        driver = self.driver
        self.quality_inspection_menu()
        driver.find_element_by_xpath("(//button[@type='button'])[6]").click() #点击任务状态下拉框
        driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[3]/span").click() #取消选择'待质检'
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[7]/span").click() #选择待结算
        time.sleep(3)
        driver.find_element_by_xpath("//table[@id='dg']/tbody/tr[1]/td[15]/input").click() #选择勾选框 
        driver.find_element_by_link_text(u"批量结算（不付款）").click() #点击批量结算不付款
        time.sleep(2)
        #self.imgname = time.strftime("%Y_%m_%d_%H_%M_%S") + '_settle_and_no_pay.png'       
        self.assertEqual(u"完成结算质检!", self.close_alert_and_get_its_text())

    def atest_re_examine_successful(self): #质检不通过-复审通过
        driver = self.driver
        self.quality_inspection_menu()
        driver.find_element_by_xpath("(//button[@type='button'])[6]").click() #点击任务状态下拉框
        driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[3]/span").click() #取消选择'待质检'
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[4]/span").click() #点击选择'质检不通过'
        time.sleep(3)
        driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[14]/div/button").click() #点击操作按钮
        driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[14]/div/ul/li[5]/a/small").click() #点击复审(质检不通过)
        driver.find_element_by_xpath("//div[@id='task-online-check-nopass-review-status-radios']/label").click() #点击复审通过，回到待质检
        self.re_examine_fail_remark('Autotest re-examine successful') #备注输入框输入内容
        driver.find_element_by_xpath("//div[@id='task-online-check-nopass-review']/div/div[3]/span[2]").click() #点击确定按钮
        time.sleep(2)
        #self.imgname = time.strftime("%Y_%m_%d_%H_%M_%S") + '_re_examine_successful.png'
        self.assertEqual(u"完成质检不通过复审!", self.close_alert_and_get_its_text())

    def atest_re_examine_unsuccessful(self): #质检不通过-复审不通过
        driver = self.driver
        self.quality_inspection_menu()
        driver.find_element_by_xpath("(//button[@type='button'])[6]").click() #点击任务状态下拉框
        driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[3]/span").click() #取消选择'待质检'
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[4]/span").click() #点击选择'质检不通过'
        time.sleep(3)
        driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[14]/div/button").click() #点击操作按钮
        driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[14]/div/ul/li[5]/a/small").click() #点击复审(质检不通过)
        driver.find_element_by_xpath("//div[@id='task-online-check-nopass-review-status-radios']/label[2]").click() #点击不予通过，回到任务池
        self.re_examine_fail_remark('Autotest re-examine unsuccessful')
        driver.find_element_by_xpath("//div[@id='task-online-check-nopass-review']/div/div[3]/span[2]").click() #点击确定按钮
        time.sleep(2)
        #self.imgname = time.strftime("%Y_%m_%d_%H_%M_%S") + '_re_examine_unsuccessful.png'
        self.assertEqual(u"完成质检不通过复审!", self.close_alert_and_get_its_text())

    def test_reapprove_successful(self): #审批不通过-复审通过
        driver = self.driver
        self.quality_inspection_menu()
        driver.find_element_by_xpath("(//button[@type='button'])[6]").click() #点击任务状态下拉框
        driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[3]/span").click() #取消选择'待质检'
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[6]/span").click() #点击选择'审批不通过'
        time.sleep(3)
        driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[14]/div/button").click() #点击操作按钮
        driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[14]/div/ul/li[5]/a/small").click() #点击复审(审批不通过)
        driver.find_element_by_xpath("//div[@id='task-test-check-nopass-review-status-radios']/label").click() #点击复审通过，回到待审批
        self.reapprove_remark('Autotest reapprove successful') #备注输入框输入内容
        driver.find_element_by_xpath("//div[@id='task-test-check-nopass-review']/div/div[3]/span[2]").click() #点击确定按钮
        time.sleep(2)
        #self.imgname = time.strftime("%Y_%m_%d_%H_%M_%S") + '_reapprove_successful.png'
        self.assertEqual(u"完成审批不通过复审!", self.close_alert_and_get_its_text()) #弹框提示比对  提示有误

    def test_reapprove_unsuccessful(self): #审批不通过-不予通过
        driver = self.driver
        self.quality_inspection_menu()
        driver.find_element_by_xpath("(//button[@type='button'])[6]").click() #点击任务状态下拉框
        driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[3]/span").click() #取消选择'待质检'
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[6]/span").click() #点击选择'审批不通过'
        time.sleep(3)
        driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[14]/div/button").click() #点击操作按钮
        driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[14]/div/ul/li[5]/a/small").click() #点击复审(审批不通过)
        driver.find_element_by_xpath("//div[@id='task-test-check-nopass-review-status-radios']/label[2]").click() #点击不予通过，回到任务池
        self.reapprove_remark('Autotest reapprove unsuccessful')
        driver.find_element_by_xpath("//div[@id='task-test-check-nopass-review']/div/div[3]/span[2]").click() #点击确定按钮
        time.sleep(3)
        #self.imgname = time.strftime("%Y_%m_%d_%H_%M_%S") + '_reapprove_unsuccessful.png'
        self.assertEqual(u"完成审批不通过复审!", self.close_alert_and_get_its_text()) #弹框提示比对  提示有误

    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException as e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException as e: return False
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
    def screenshot(self):

    
    def tearDown(self):
        #filenames = r'E:\\test\\selenium project\\photo\\' + self.imgname #图片路径
        #self.driver.get_screenshot_as_file(filenames) #屏幕截图
        #time.sleep(1)
        self.driver.quit()

if __name__ == "__main__":
    testunit = unittest.TestSuite()
    #testunit.addTest(JMToolTestCase('test_quality_inspection_successful_and_no_pay'))
    #testunit.addTest(JMToolTestCase('test_examine_and_approve_successful'))
    #testunit.addTest(JMToolTestCase('test_examine_and_approve_unsuccessful'))
    #testunit.addTest(JMToolTestCase('test_settle_and_pay_money'))
    #testunit.addTest(JMToolTestCase('test_settle_and_no_pay'))
    #testunit.addTest(JMToolTestCase('test_re_examine_successful'))
    testunit.addTest(JMToolTestCase('test_re_examine_unsuccessful'))
    #testunit.addTest(JMToolTestCase('test_reapprove_successful'))
    testunit.addTest(JMToolTestCase('test_reapprove_unsuccessful'))
    nowtime = time.strftime("%Y_%m_%d_%H_%M_%S")
    reportname = r'E:\\test\\selenium project\\webTest\\report\\'+nowtime+'report.html'
    fp = open(reportname,'wb')

    runner = HTMLTestRunner(stream=fp,title='emlog登陆测试',description='执行详情')
    runner.run(testunit)