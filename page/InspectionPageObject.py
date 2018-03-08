import sys, unittest, time, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select


class InspectionPage:
    #切换任务状态到待结算
    def switch_status_to_wait_to_settlement(self,driver):
        driver.find_element_by_xpath("//div[@class='am-g am-margin-top-sm']/div/div/button").click() #点击任务状态下拉框
        driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[3]/span").click() #取消选择'待质检'
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[7]/span").click() #选择待结算
        time.sleep(3)

    #切换任务状态到待审批
    def switch_status_to_wait_to_approve(self,driver):
        driver.find_element_by_xpath("(//button[@type='button'])[6]").click()  # 点击任务状态下拉框
        driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[3]/span").click()  # 取消选择'待质检'
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[5]/span").click()  # 点击选择'待审批'
        time.sleep(3)


    #切换任务状态到审批不通过
    def switch_status_to_approve_not_pass(self,driver):
        driver.find_element_by_xpath("(//button[@type='button'])[6]").click() #点击任务状态下拉框
        driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[3]/span").click() #取消选择'待质检'
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[6]/span").click() #点击选择'审批不通过'
        time.sleep(4)

    #切换任务状态到质检不通过
    def switch_status_to_quality_inspection_not_pass(self,driver):
        driver.find_element_by_xpath("(//button[@type='button'])[6]").click() #点击任务状态下拉框
        driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[3]/span").click() #取消选择'待质检'
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='am-selected am-dropdown  am-active']/div/ul/li[4]/span").click() #点击选择'质检不通过'
        time.sleep(4)

	#点击质检菜单函数
    def quality_inspection_menu(self,driver):
        driver.find_element_by_xpath("//div[@id='admin-offcanvas']/div/ul/li[5]/a/span[2]").click() #点击任务质检菜单
        time.sleep(1)
        driver.find_element_by_xpath("//ul[@id='collapse-nav10']/li/a/span[2]").click() #点击质检菜单
        time.sleep(1)

    #审批-备注框输入函数
    def approve_remark(self,driver,con_approve_remark): 
        driver.find_element_by_id("task-test-check-remark").click()
        driver.find_element_by_id("task-test-check-remark").clear()
        driver.find_element_by_id("task-test-check-remark").send_keys(con_approve_remark)

    #复审不通过-备注框输入函数
    def re_examine_fail_remark(self,driver,con_re_examine_fail_remark):
        driver.find_element_by_id("task-online-check-nopass-review-remark").click()
        driver.find_element_by_id("task-online-check-nopass-review-remark").clear()
        driver.find_element_by_id("task-online-check-nopass-review-remark").send_keys(con_re_examine_fail_remark)
    #审批不通过-备注框输入函数
    def reapprove_remark(self,driver,con_reapprove_remark):
        driver.find_element_by_id("task-test-check-nopass-review-remark").click()
        driver.find_element_by_id("task-test-check-nopass-review-remark").clear()
        driver.find_element_by_id("task-test-check-nopass-review-remark").send_keys(con_reapprove_remark)

    #删除备注输入框函数
    def delete_remark(self,driver,con_delete_remark):
        driver.find_element_by_id("task-delete-remark").click()
        driver.find_element_by_id("task-delete-remark").clear()
        driver.find_element_by_id("task-delete-remark").send_keys(con_delete_remark)

    #质检不通过备注框输入函数
    def inspection_not_pass_remark(self,driver,con_inspection_not_pass_remark):
        driver.find_element_by_id("task-online-check-remark").click()
        driver.find_element_by_id("task-online-check-remark").clear()
        driver.find_element_by_id("task-online-check-remark").send_keys(con_inspection_not_pass_remark)

    #搜索框输入函数
    def search_enter(self,driver,con_search_enter):
        driver.find_element_by_id("search-text").click()
        driver.find_element_by_id("search-text").clear()
        driver.find_element_by_id("search-text").send_keys(con_search_enter)

    #质检页面精确匹配搜索
    def inspection_page_accurate_search(self,driver):
        driver.find_element_by_xpath("(//button[@type='button'])[11]").click() #点击选择匹配方式
        time.sleep(1)
        driver.find_element_by_xpath("//div[@class='am-u-sm-12 am-u-md-2 am-u-sm-offset-2']/div/div/ul/li[2]/span").click() #选择精确匹配
        driver.find_element_by_xpath("(//button[@type='button'])[12]").click() #点击选择搜索类型
        time.sleep(1)

    #质检操作函数
    def inspection_action(self,driver):
        #获取当前标签句柄
        first_handle = driver.current_window_handle
        driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[14]/a/small").click() #点击操作-质检
        all_handles = driver.window_handles  # 获取所有窗口句柄
        for handle in all_handles:    #判断当前窗口句柄，切换窗口
            if handle != first_handle:
                driver.switch_to_window(handle)
        #切换窗口，进行质检操作

    #质检结果查看操作函数    
    def inspection_check_action(self,driver):
        #获取当前标签句柄
        first_handle = driver.current_window_handle
        driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[14]/div/button").click() #点击操作栏-操作
        driver.find_element_by_xpath("//table[@id='dg']/tbody/tr/td[14]/div/ul/li[7]/a/small").click() #点击质检结果查看按钮
        all_handles = driver.window_handles  # 获取所有窗口句柄
        for handle in all_handles:    #判断当前窗口句柄，切换窗口
            if handle != first_handle:
                driver.switch_to_window(handle)
        #切换窗口，进行质检操作