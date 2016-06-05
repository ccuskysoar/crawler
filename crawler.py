from bs4 import BeautifulSoup
import requests
import HTMLParser
import time
#from urllib.parse import urlsplit
import urllib2
import argparse
url_list = list()

def crawler(url):
    url_list.append(url)
    while len(url_list) > 0:
        page = urllib2.urlopen(url_list[0])
        #print(page.read())
        soup = BeautifulSoup(page,"lxml")
        
        #find next url
        for i in soup.find_all('a'):
            #link = i['href']
            link = i.attrs["href"] if "href" in i.attrs else ''
            if link[0:4] == 'http':
               print(link)
               url_list.append(link)
            elif link[0:1]==('.'):
               link = url_list[0] + link[1:]
               print(link)
               url_list.append(link)
            #print(link)
        #print(url_list)
        url_list.pop(0)
        #print(url_list)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='crawl email')
    parser.add_argument('url', help='input url to crawl')
    args = parser.parse_args()
    crawler(args.url)
    #crawler('http://www.ccu.edu.tw/')
