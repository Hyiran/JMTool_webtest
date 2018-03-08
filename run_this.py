# coding:utf-8
import unittest
import os
import HTMLTestRunner

# python2.7要是报编码问题，就加这三行，python3不用加
#import sys
#reload(sys)
#sys.setdefaultencoding('utf8')

cur_path = os.path.dirname(os.path.realpath(__file__))
print(cur_path)
#case_path = os.path.join(cur_path, "test_case")        # 测试用例的路径
case_path = os.path.join(os.getcwd(),"test_case")
print(case_path)
#report_path = os.path.join(cur_path, "report")  # 报告存放路径
report_path = os.path.join(os.getcwd(),"report")
print(report_path)

#retry修改用例失败之后，重试次数
if __name__ == "__main__":
    discover = unittest.defaultTestLoader.discover(case_path,"test_r2*.py")
    print(discover)
    run = HTMLTestRunner.HTMLTestRunner(title="可以装逼的测试报告",
                                            description="测试用例参考",
                                            stream=open(report_path+"\\result.html", "wb"),
                                            verbosity=2,
                                            retry=1)

    #run.run(discover)
