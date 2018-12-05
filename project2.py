# !-*- coding:utf-8 -*-

from tkinter import *
import requests
from bs4 import BeautifulSoup
import sys
import smtplib
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
import shutil
from sender import sender, passWord


class downLoad():
    def __init__(self):
        self.root = Tk()
        self.root.geometry('350x200')
        self.root.title("笔趣看小说下载助手")

        Label(self.root, text="    Book_url").grid(row=0, sticky=W)
        Label(self.root, text="    send_email").grid(row=1, sticky=W)
        self.e1 = Entry(self.root)
        self.e2 = Entry(self.root)
        button1 = Button(self.root, text=" download", command=self.download)
        button2 = Button(self.root, text="     send    ", command=self.send_email)
        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        button1.grid(row=0, column=2)
        button2.grid(row=1, column=2)

        Label(self.root, text="本插件仅适用于笔趣看小说下载，"
                              "请输入您想下载的小说url，如'http://www.biqukan.com/0_178/'",
              wraplength=170).grid(columnspan=3)

        self.root.mainloop()


#定义一个下载小说的函数
    def get_download_url(self):
        self.server = 'http://www.biqukan.com/'
        self.target = self.e1.get()
        # self.target = 'http://www.biqukan.com/0_178/'
        self.names = []  # chapter name
        self.urls = []  # chapter link
        self.nums = 0  # chapter count

        req = requests.get(url=self.target)
        html = req.text
        div_bf = BeautifulSoup(html, 'html.parser')  # BeautifulSoup 对象提取相应数据-div
        div = div_bf.find_all('div', class_='listmain')  # 筛选出div且class标签-listmain
        a_bf = BeautifulSoup(str(div[0]), 'html.parser')
        # 在第一次筛选的div里面再次筛选a标签
        a = a_bf.find_all('a')  # 找到所有a标签
        self.nums = len(a[15:])
        for each in a[15:]:
            self.names.append(each.string)
            self.urls.append(self.server + each.get('href'))
            # 检查：a标签由server + href组成

    def get_contents(self, target):
        req = requests.get(url=target)
        html = req.text
        bf = BeautifulSoup(html, 'html.parser')
        texts = bf.find_all('div', class_='showtxt')
        texts = texts[0].text.replace('\xa0' * 8, '\n\n')
        return texts

    def writer(self, name, path, text):
        with open(path, 'a', encoding='utf-8') as f:
            f.write(name + '\n')
            f.writelines(text)
            f.write('\n\n')
        shutil.make_archive('G:/biqu_book','zip',r'G:/biqu_book')

    def download(self):
        self.get_download_url()
        print('开始下载:')
        for i in range(self.nums):
            self.writer(self.names[i], 'G:/biqu_book/text1.txt', self.get_contents(self.urls[i]))
            sys.stdout.write("  已下载:%.2f%%" % float(i / self.nums * 100) + '\r')
            sys.stdout.flush()
        print('下载完成')

#定义一个发送邮件的函数：
    def send_email(self):
        mail_host = 'smtp.qq.com'
        receivers = []
        receivers.append(self.e2.get())
        print('send To :', receivers[0:])

        msg = MIMEMultipart()
        msg['Subject'] = input(u'请输如邮件主题:')
        # 发送方信息
        msg['From'] = sender
        # 邮件正文是MIMEText:
        msg_content = input(u'请输入邮件主内容:')
        msg.attach(MIMEText(msg_content, 'plain', 'utf-8'))
        # 添加附件就是加上一个MIMEBase，从本地读取一个文件:
        with open(u'G:/biqu_book.zip', 'rb') as f:
            # 设置附件的MIME和文件名，这里是txt类型,可以换png或其他类型:
            mime = MIMEBase('zip', 'zip', filename='biqu.zip')
            # 加上必要的头信息:
            mime.add_header('Content-Disposition', 'attachment', filename='biqu.zip')
            mime.add_header('Content-ID', '<0>')
            mime.add_header('X-Attachment-Id', '0')
            # 把附件的内容读进来:
            mime.set_payload(f.read())
            # 用Base64编码:
            encoders.encode_base64(mime)
            # 添加到MIMEMultipart:
            msg.attach(mime)

        # 登录并发送邮件
        try:
            # QQsmtp服务器的端口号为465或587
            s = smtplib.SMTP_SSL(mail_host, 465)
            s.set_debuglevel(1)     #打印出和SMTP服务器交互的所有信息
            s.login(sender, passWord)
            # 给receivers列表中的联系人逐个发送邮件
            for item in receivers:
                msg['To'] = to = item
                s.sendmail(sender, to, msg.as_string())
                print('Success!')
            s.quit()
            print("All e_mails have been sent over!")
        except smtplib.SMTPException as e:
            print("Falied!"+ "\n" + "Reason:",  e)


#实例化：
download = downLoad()

