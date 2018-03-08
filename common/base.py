import sys, unittest, time, os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

class basic_def(object):
    '''常用函数'''
    #登录函数
    def login(self,driver,user,pw):
        driver.find_element_by_id("username").clear()
        driver.find_element_by_id("username").send_keys(user)
        driver.find_element_by_id("password").clear()
        driver.find_element_by_id("password").send_keys(pw)
        driver.find_element_by_id("password").send_keys(Keys.ENTER)
    #审批-备注框输入函数
    def approve_remark(self,driver,con_approve_remark): 
        driver.find_element_by_id("task-test-check-remark").click()
        driver.find_element_by_id("task-test-check-remark").clear()
        driver.find_element_by_id("task-test-check-remark").send_keys(con_approve_remark)
    #点击质检菜单函数
    def quality_inspection_menu(self,driver):
        driver.find_element_by_xpath("//div[@id='admin-offcanvas']/div/ul/li[5]/a/span[2]").click() #点击任务质检菜单
        time.sleep(1)
        driver.find_element_by_xpath("//ul[@id='collapse-nav10']/li/a/span[2]").click() #点击质检菜单
        time.sleep(1)
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

    #业务执行-精确匹配ID，搜索框输入函数
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