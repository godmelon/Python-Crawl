# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 16:13:36 2018

@author: wangzhaohua
"""

from lxml import etree
import requests

url = 'http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-all-0-0-1-1'

headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, \
        like Gecko) Chrome/59.0.3071.115 Safari/537.36"
        }
data = requests.get(url, headers=headers).text

s = etree.HTML(data)

items = s.xpath('//*[@id="sortRanking"]/div')

with open('dangdang.csv', 'w') as outputfile:
    for item in items:
        book_title = item.xpath('./a/text()')
        book_url = item.xpath('./a/@href')
        
        if len(book_url) > 0:
            href = book_url[0]
            title = book_title[0]
            a = href[41:46]
            
            for page in range(1,26):
                per_url = 'http://bang.dangdang.com/books/fivestars/{}.00.00.00.00-all-0-0-1-{}'.format(a, page)
                per_data = requests.get(per_url, headers=headers).text
                per_s = etree.HTML(per_data)
                
                try:
                    print("page {}, title {}".format(page, title))
                    file = per_s.xpath('/html/body/div[3]/div[3]/div[2]/ul/li')
                    
                    for per_book in file:
                        per_book_name = per_book.xpath('./div[@class="name"]/a/text()')
                        per_book_auth = per_book.xpath()
                except:
                    pass
                
                
                    
            
        
    
