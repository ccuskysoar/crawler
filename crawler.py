from bs4 import BeautifulSoup
import requests
import HTMLParser
import time
import re
import urllib2
import argparse
url_list = list()
oldUrl_list = list()

def crawler(url):
    url_list.append(url)
    while len(url_list) > 0:
        flag = checkUrl(url_list[0])
        if url_list[0] in oldUrl_list:
            url_list.pop(0)   
        elif flag == -1:
            oldUrl_list.append(url_list[0])
            url_list.pop(0)
        else:
            if isConnect(url_list[0]):
                page = urllib2.urlopen(url_list[0])
                soup = BeautifulSoup(page,'lxml')
                ###find emails in the page###
                email = re.findall(r'[A-Za-z0-9_\-\.]+\@[A-Za-z0-9_\-\.]+\.[A-Za-z]{2,4}', soup.prettify())
                for j in email:
                   print(j)
                ###find next page### 
                for i in soup.find_all('a'):
                    link = i.attrs['href'] if "href" in i.attrs else ''
                    if link[0:4] == 'http':
                        if link in oldUrl_list:
                            pass
                        else:
                            url_list.append(link)
                    elif link[0:1]==('.'):
                        if link in oldUrl_list:
                            pass
                        else:
                            link = url_list[0] + link[1:]
                            url_list.append(link)    
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
    elif url[-3:]=='mp3' or url[-3:]=='mp4' or url[-3:]=='wmv' or url[-3:]=='avi' or url[-3:] =='flv':
        return -1   
    elif url[-3:]=='jpg' or url[-3:]=='png' or url[-3:]=='gif':
        return -1
    elif url[-3:]=='zip' or url[-3:]=='rar':
        return -1
    else:
        return 1

def isConnect(url):
    try:
        urllib2.urlopen(url)
    #except urllib2.HTTPError, e:
    except :
        print(url)
        return False
    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='crawl email')
    parser.add_argument('url', help='input url to crawl')
    args = parser.parse_args()
    crawler(args.url)
