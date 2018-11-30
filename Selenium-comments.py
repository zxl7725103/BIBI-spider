from selenium import webdriver
# Keys()类提供了键盘上几乎所有按键的方法，这个类可用来模拟键盘上的按键，包括各种组合键
from selenium.webdriver.common.keys import Keys
# 将用pandas中的DataFrame（一种二维的表格型数据结构）记录爬下的数据
import pandas as pd
from datetime import datetime
import numpy as np
import time
import os

def gethtml(url):
	#指定浏览器为Chrome
    browser = webdriver.Chrome()
    # 访问页面
    browser.get(url)
    #隐式等待10秒
    browser.implicitly_wait(10)
    return(browser)
# 指定要爬的网址：bilibili刀剑神域主页
url = 'https://www.bilibili.com/bangumi/media/md139332/?spm_id_from=666.10.b_62616e67756d695f6d65646961.1#short'
browser = gethtml(url)
print('连接成功，开始爬数据')

shortcomment_str=browser.find_element_by_xpath('//*[@id="app"]/div[2]/div[1]/ul/li[3]').text
shortcomment_num=int(shortcomment_str.split()[2])

nowcomment_num=len(browser.find_elements_by_class_name('clearfix'))
while nowcomment_num< shortcomment_num:
    html = browser.find_element_by_tag_name('html')
    # 模拟键盘替我们不断滑到页面底部，刷出更多数据
    html.send_keys(Keys.END)
    # 获取当前页面显示的短评总数
    nowcomment_num = len(browser.find_elements_by_class_name('clearfix'))
    print(nowcomment_num)

authors=browser.find_elements_by_class_name('review-author-name')
for i in range(len(authors)):
    lstauthors=authors[i].text

# 抓取点赞数
stars=browser.find_elements_by_class_name('review-stars')
for i in range(len(stars)):
    lststars=len(stars[i].find_elements_by_class_name('icon-star-light'))
    print(lststars)
#抓取评论内容
comments=browser.find_elements_by_class_name('review-content')
for i in range(len(comments)):
    lstcomments=comments[i].text

#抓取评论时间
review_time = browser.find_elements_by_class_name('review-author-time')
lstReviewTime = [review_time[i].text for i in range(len(review_time))]

# 组成一张comments表
comments = pd.DataFrame([lstauthors, lststars, lstcomments, lstReviewTime])
comments = comments.T
comments.columns = ['author', 'stars', 'comment', 'time']
comments.to_csv('my_data.csv', index=False)
comments.to_csv('my_data.csv', encoding='utf_8_sig')
