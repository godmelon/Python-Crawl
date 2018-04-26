# -*- coding: utf-8 -*-
"""
Created on Wed Apr 25 16:13:36 2018

@author: wangzhaohua
"""

from lxml import etree
import requests
import time

url = 'http://bang.dangdang.com/books/fivestars/01.00.00.00.00.00-all-0-0-1-1'

headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, \
        like Gecko) Chrome/59.0.3071.115 Safari/537.36"
        }
data = requests.get(url, headers=headers).text

s = etree.HTML(data)

items = s.xpath('//*[@id="sortRanking"]/div[3]')

with open('dangdang.txt', 'w', encoding='utf-8') as outputfile:
    for item in items:
        book_title = item.xpath('./a/text()')
        book_url = item.xpath('./a/@href')
        
        if len(book_url) > 0:
            href = book_url[0]
            title = book_title[0]
            a = href[41:46]
            
            for page in range(1,4):
                per_url = 'http://bang.dangdang.com/books/fivestars/{}.00.00.00.00-all-0-0-1-{}'.format(a, page)
                per_data = requests.get(per_url, headers=headers).text
                per_s = etree.HTML(per_data)
                print(per_url)
                print("page {}, title {}".format(page, title))
                file = per_s.xpath('//ul[@class="bang_list clearfix bang_list_mode"]/li')
                time.sleep(2)
                
                for per_book in file:
                    per_book_name = per_book.xpath('./div[@class="name"]/a/text()')
                    print(per_book_name)
                    per_book_auth = per_book.xpath('string(./div[@class="publisher_info"][1])')
                    print(per_book_auth)
                    per_book_pinglun = per_book.xpath('./div[@class="star"]/a/text()')[0].strip("条评论")  #清楚尾部“条评论”字符串
                    print(per_book_pinglun)
                    per_book_wuxing = per_book.xpath('./div[@class="biaosheng"]/span/text()')[0].strip("次")
                    print(per_book_wuxing)
                    per_book_price_now = per_book.xpath('./div[8]/p[1]/span[1]/text()')[0]
                    print(per_book_price_now)
                    per_book_price_bef = per_book.xpath('./div[8]/p[1]/span[2]/text()')[0]
                    print(per_book_price_bef)
                    
                    outputfile.write('{},{},{},{},{},{}\n'.format(per_book_name,per_book_auth,\
                                     per_book_pinglun,per_book_wuxing,per_book_price_now,per_book_price_bef))
                    