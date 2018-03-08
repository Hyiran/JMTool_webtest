import smtplib,os,time,unittest
from selenium import webdriver
from HTMLTestRunner import HTMLTestRunner
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart

def send_mail(reportname):
	smtpHost = 'smtp.qq.com'
	smtpPort = '25'
	sslPort = '465'
	user = '103165967'
	password = 'ufwvelbejnarbhdd'
	sender = '103165967@qq.com'
	receiver = 'dzsone@163.com'
	subject = 'test'
	sendfile = open(reportname,'rb').read()
	att = MIMEText(sendfile,'base64','utf-8')
	att ["Content-Type"]='application/octet-stream'
	att["Content-Disposition"]='attachment;filename=Autotest_report.html'
	msgRoot=MIMEMultipart('related')
	msgRoot['Subject']=nowtime + "_JMTool自动化测试报告"
	msgRoot.attach(att)
	smtp=smtplib.SMTP_SSL(smtpHost,sslPort)
	smtp.ehlo()
	smtp.login(user,password)
	smtp.sendmail(sender,receiver,msgRoot.as_string())
	smtp.quit()


def new_report(testreportdir):
	lists = os.listdir(testreportdir)
	lists.sort(key=lambda fn:os.path.getmtime(testreportdir+"\\"+fn))
	newfile=os.path.join(testreportdir,lists[-1])
	print(newfile)
	return newfile

if __name__ == '__main__':
	testdir = r'E:\\test\\selenium project\\webTest\\test_case'
	testreportdir = r'E:\\test\\selenium project\\webTest\\report'
	discover = unittest.defaultTestLoader.discover(testdir,pattern = 'test_JMTool_inspection_m*.py')
	nowtime = time.strftime("%Y_%m_%d_%H_%M_%S")
	reportname = testreportdir + nowtime +'_JMTool_Autotest_report.html'
	#print(reportname+"123")
	fp = open(reportname,'wb')
	runner = HTMLTestRunner(stream=fp,title="JMToolm冒烟测试报告",description="测试用例执行详情")
	runner.run(discover)
	fp.close()
	new_reportfile = new_report(testreportdir)
	send_mail(new_reportfile)