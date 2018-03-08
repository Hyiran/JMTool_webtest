from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re, sys, os
from page.InspectionPageObject import InspectionPage
from page.BusinessExecutionPageObject import BusinessExecutionPage
from page.TaskControlPageObject import TaskControlPage
from page.LoginPage import LoginPage
from common.Log import logger
from common.config import Config,CONFIG_FILE,LOG_PATH,REPORT_PATH,CASE_PATH,PAGE_PATH
from common.mail import Email
from common.HTMLTestRunner import HTMLTestRunner


if __name__ == '__main__':
    discover = unittest.defaultTestLoader.discover(CASE_PATH,"test_JMTool_r*.py") #执行测试用例路径下的匹配脚本
    nowtime = time.strftime("%Y-%m-%d-%H-%M-%S")
    report = REPORT_PATH + '\\' + nowtime + '_JMTool_report.html'
    with open(report, 'wb') as f:
        runner = HTMLTestRunner(f, verbosity=2, title='JMTool自动化测试报告', description='自动化测试用例参考')
        runner.run(discover)
    e = Email(title='JMTool自动化测试报告',
              message='这是今天的测试报告，请查收！',
              receiver='jeff.shan@nf-3.com', #; saeed.yang@nf-3.com ; jc.lin@nf-3.com ; c.zhang@nf-3.com',
              server='smtp.163.com',
              sender='dzsone@163.com',
              password='szhihong91',
              path=report
              )
    e.send()
  