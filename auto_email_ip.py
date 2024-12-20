#!/usr/local/bin/python3
# coding=utf-8

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from urllib import request
from collections import Counter
import re
import time
import threading
import logging

textList = []
sendIPAddress = ''

# Configure logging
logging.basicConfig(filename='auto_email_ip.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def log_message(message):
    logging.info(message)

def sendIP(content):
    # config
    host = 'smtp.***.com'
    port = 465
    sender = '***@***.***'
    receiver = ['***@***.***',
                '***@***.***', 
                '***@***.***']
    pwd = '***'  # Password
    # core
    msg = MIMEText(content, _subtype='plain', _charset='utf-8')
    msg['subject'] = 'IP changed. Please handle it quickly'
    msg['from'] = sender
    msg['to'] = ",".join(receiver)

    try:
        hero = smtplib.SMTP_SSL(host=host, port=port)
        hero.login(sender, pwd)
        hero.sendmail(sender, receiver, msg.as_string())
    except Exception as e:
        log_message(f'Error sending IP: {str(e)}')
        print('error:', str(e))
    else:
        log_message('IP sent successfully.')
        print('IP is sended successly.')


def getIP():
    urls = ['https://api.ipify.org',
            'https://icanhazip.com',
            'https://ipv4.ddnspod.com',
            'https://checkip.amazonaws.com']
    #Simulate browser access to avoid being blocked by the site
    header = {
        'Connection': 'Keep-Alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'
    }
    ips = []
    for url in urls:
        try:
            req = request.Request(url, headers=header)
            html = request.urlopen(req).read()
            print('request:' + url)
            content = html.decode('utf-8')  # utf-8 decode
            pattern = re.compile(
                r'((?:(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d)))\.){3}(?:25[0-5]|2[0-4]\d|((1\d{2})|([1-9]?\d))))', re.M | re.I)
            ipAddress = pattern.search(content).group(0)
        except Exception as e:
            textList.append('error:' + str(e))
            print('error:' + str(e))
        else:
            # textList.append(url)
            # textList.append(ipAddress)
            ips.append(ipAddress)
            print('success:' + url + ":" + ipAddress)
    ipsCounter = Counter(ips)
    if len(ipsCounter) > 0:
        ip = ipsCounter.most_common()[0][0]
        return ip

def getipv6():
    # get ipv6
    urls = [
        'https://ipv6.ddnspod.com/',
        'https://ipv6.icanhazip.com/',
        'https://v6.ident.me/',
        'https://speed.neu6.edu.cn/getIP.php'
    ]
    header = {
        'Connection': 'Keep-Alive',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36'
    }
    ipv6s = []
    for url in urls:
        try:
            req = request.Request(url, headers=header)
            html = request.urlopen(req).read()
            print('request:' + url)
            content = html.decode('utf-8')  # utf-8 decode
            pattern = re.compile(
                r'([0-9a-fA-F]{1,4}(:[0-9a-fA-F]{1,4}){7})', re.M | re.I)
            ipv6 = pattern.search(content).group(0)
        except Exception as e:
            textList.append('error:' + str(e))
            print('error:' + str(e))
        else:
            # textList.append(url)
            # textList.append(ipv6)
            ipv6s.append(ipv6)
            print('success:' + url + ":" + ipv6)
    ipv6sCounter = Counter(ipv6s)
    if len(ipv6sCounter) > 0:
        ipv6 = ipv6sCounter.most_common()[0][0]
        return ipv6


def checkIP():
    global sendIPAddress
    log_message('Checking IP...')
    print('Checking...')
    # nowIp = getIP() #ipv4
    nowIp = getipv6() #ipv6

    if sendIPAddress != nowIp:
        sendIPAddress = nowIp
        log_message(f'IP changed to {nowIp}')
        print('IP changed '+nowIp)
        nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        textList.insert(0, nowtime)
        textList.insert(1, 'IP: ' + sendIPAddress)
        jellyfin = 'Jellyfin: ' + 'http://'+ sendIPAddress + ':8096/web/index.html'
        textList.insert(2, jellyfin)
        Alist = 'Alist: ''http://' + sendIPAddress + ':5244'
        textList.insert(3, Alist)
        content = '\n'.join(textList)
        sendIP(content)
    else:
        log_message('IP not changed')
        print('IP not change')

    textList.clear()
    t = threading.Timer(66.0, checkIP)
    t.start()

def clear_log():
    with open('auto_email_ip.log', 'w'):
        pass
    log_message('Log cleared')
    t = threading.Timer(86400, clear_log)  # 24 hours / 86400 seconds 清除一次日志
    t.start()
    

if __name__ == "__main__":
    log_message('started')
    print("start")
    nowtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    textList.insert(0, nowtime)
    # sendIPAddress = getIP() #获取ipv4
    sendIPAddress = getipv6() #获取ipv6
    textList.insert(1, 'IP: ' + sendIPAddress)
    jellyfin = 'Jellyfin: ' + 'http://'+ sendIPAddress + ':8096/web/index.html'
    textList.insert(2, jellyfin)
    Alist = 'Alist: ''http://' + sendIPAddress + ':5244'
    textList.insert(3, Alist)
    # 可以添加更多的便捷链接
    content = '\n'.join(textList)
    print(content)
    # sendIP(content)
    textList.clear()
    clear_log()

    t1 = threading.Timer(60.0, checkIP) # 1分钟检查一次
    # t = threading.Timer(14400.0, checkIP) # 4小时检查一次
    t1.start()

    # Start the log clearing timer