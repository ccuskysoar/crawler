from bs4 import BeautifulSoup
import requests
import HTMLParser
import time
import re
import urllib2
import argparse
import socket
url_list = list()
oldUrl_list = list()

def crawler(url):
    url_list.append(url)
    mailNumber = 0
    while len(url_list) > 0:
        flag = checkUrl(url_list[0])
        if url_list[0] in oldUrl_list:
            url_list.pop(0)   
        elif flag == -1:
            oldUrl_list.append(url_list[0])
            url_list.pop(0)
        else:
            if isConnect(url_list[0]):
                page = urllib2.urlopen(url_list[0].encode('utf-8'),timeout=5)
                soup = BeautifulSoup(page,'lxml')
                ###find emails in the page###
                email = set(re.findall(r'[A-Za-z0-9_\-\.]+\@[A-Za-z0-9_\-\.]+\.[A-Za-z]{2,4}', soup.prettify()))
                for j in email:
                   print(j)
                   mailNumber= mailNumber + 1
                print('                    already crawled %s mails.' %mailNumber)
                ###find next page### 
                for i in soup.find_all('a'):
                    link = i.attrs['href'] if "href" in i.attrs else ''
                    if link[0:4] == 'http':
                        if link in oldUrl_list:
                            pass
                        else:
                            url_list.append(link)
                    elif link[0:2]=='./':
                        if url_list[0][-1:]=='/':
                           link = url_list[0] + link[2:] 
                        else:
                            link = url_list[0] + link[1:]
                        url_list.append(link)
                    elif link[0:1]=='/':
                        if url_list[0][-1:]=='/':
                            link = url_list[0] + link[1:]
                        else:
                            link = url_list[0] + link
                        url_list.append(link) 
                    elif link[0:1]=='#':
                        pass   
                    else:
                       if url_list[0][-1:]=='/':
                           link = url_list[0] + link
                       else:
                           link = url_list[0] + '/' + link
                       url_list.append(link)
                oldUrl_list.append(url_list[0])
                url_list.pop(0)
            else:
                oldUrl_list.append(url_list[0])
                url_list.pop(0)

def checkUrl(url):
    if url[-3:]=='pdf' or url[-4:]=='pptx' or url[-3:]=='ppt' or url[-4:]=='docx' or url[-3:]=='doc':
        return -1
    elif url[-3:]=='mp3' or url[-3:]=='mp4' or url[-3:]=='mpg' or url[-3:]=='avi' or url[-4:] =='rmvb':
        return -1   
    elif url[-3:]=='jpg' or url[-3:]=='png' or url[-3:]=='gif'or url[-3:]=='zip' or url[-3:]=='rar':
        return -1
    else:
        return 1

def isConnect(url):
    try:
        urllib2.urlopen(url.encode('UTF-8'),timeout=5)
    except urllib2.HTTPError, e:
        return False
    except urllib2.URLError, e:
        return False
    except socket.timeout, e:
        return False
    except socket.error, e:
        return False
    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='crawl email')
    parser.add_argument('url', help='input url to crawl')
    args = parser.parse_args()
    crawler(args.url)
