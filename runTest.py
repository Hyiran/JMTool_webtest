import smtplib,os,time,unittest
from selenium import webdriver
from HTMLTestRunner import HTMLTestRunner
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart

cur_path = os.path.dirname(os.path.realpath(__file__)) #当前文件路径
com_path = os.path.join(cur_path, "common") #公用脚本路径
case_path = os.path.join(cur_path, "test_case") #测试用例路径
img_path = os.path.join(cur_path, "photo") #截图存放路径
report_path = os.path.join(cur_path, "report") #测试报告路径

def send_mail(reportname): #发送邮件函数
	smtpHost = 'smtp.qq.com'
	smtpPort = '25'
	sslPort = '465'
	user = '103165967'
	password = 'ufwvelbejnarbhdd'
	sender = '103165967@qq.com'
	receiver = ['jeff.shan@nf-3.com']#,'saeed.yang@nf-3.com','jc.lin@nf-3.com','ivy.duan@nf-3.com']
	subject = 'test'
	sendfile = open(reportname,'rb').read()
	att = MIMEText(sendfile,'base64','utf-8')
	att ["Content-Type"]='application/octet-stream'
	att["Content-Disposition"]='attachment;filename=Autotest_report.html'
	msgRoot=MIMEMultipart('related')
	msgRoot['Subject']= nowtime + "_JMTool自动化测试报告"
	msgRoot.attach(att)
	smtp=smtplib.SMTP_SSL(smtpHost,sslPort)
	smtp.ehlo()
	smtp.login(user,password)
	smtp.sendmail(sender,receiver,msgRoot.as_string())
	smtp.quit()


def new_report(report_path):
	lists = os.listdir(report_path)
	lists.sort(key=lambda fn:os.path.getmtime(report_path+"\\"+fn))
	newfile=os.path.join(report_path,lists[-1])
	print(newfile)
	return newfile

if __name__ == '__main__':
	discover = unittest.defaultTestLoader.discover(case_path,"test_JMTool_inspection_b*.py") #执行测试用例路径下的匹配脚本
	nowtime = time.strftime("%Y-%m-%d-%H-%M-%S")
	reportname = report_path + "\\" + nowtime + '_JMTool_Autotest_report.html'
	fp = open(reportname,'wb')
	runner = HTMLTestRunner(title="JMToolm冒烟测试报告",description="测试用例参考",stream=fp,verbosity=2,retry=1)
	runner.run(discover)
	fp.close()
	new_reportfile = new_report(report_path)
	send_mail(new_reportfile) #调用发送邮件函数发送邮件
