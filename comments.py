import requests
import json
import pymongo

#连接数据库测试

client=pymongo.MongoClient(host='localhost',port=27017)
db=client.test
collection=db.BIBI_comments2


# 解析网址。
def Getpage_js(i):
    url='https://api.bilibili.com/x/v2/reply?callback=jQuery172027250653249242185_1542459575705&jsonp=jsonp&pn='+str(i)+'&type=1&oid=33177617&sort=0'
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36',
              'Cookie':'LIVE_BUVID=AUTO8315424591561261; fts=1542459205; buvid3=D8E2048F-2D29-440C-8ACD-62A484FF654B194524infoc; sid=ar104jas',
              'Referer':'https://www.bilibili.com/bangumi/play/ss25666/?spm_id_from=333.334.b_62696c695f62616e67756d69.20'
              }
    response=requests.get(url,headers=headers)
    if response.status_code==200 :
        return response.text
        print(response.text)
    else:
        print('wrong')

#获取评论及相关信息
def Getcomment(page):
    print(page)
    page_js=json.loads(page.strip('jQuery172027250653249242185_1542459575705()',))
    #去除不属于json 格式的文本，可以用json工具检测文本是否可以识别为json 文本，将不属于json 字典文本的去除
    if page_js['data']['replies']:
        for i in page_js['data']['replies']:
          usercomment=i['content']['message']
          username=i['member']['uname']
          userlever=i['member']['level_info']['current_level']
          userimage=i['member']['avatar']
          coments={
              '用户名':username,
              '用户等级':userlever,
              '用户头像':userimage,
              '用户评论':usercomment
          }
          result=collection.insert_one(coments)

if __name__=='__main__':
    for i in range(1,3):
        page=Getpage_js(i)
        Getcomment(page)

