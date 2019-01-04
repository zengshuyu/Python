'''
教程小结，基础爬虫
'''

import re
from urllib import request

class Spider():
    # 指定网页地址
    url = 'https://www.panda.tv/cate/overwatch'

    # 正则表达式
    root_pattern = '<div class="video-info">([\s\S]*?)</div>'
    name_pattern = '</i>([\s\S]*?)</span>'
    number_pattern = '<i class="video-station-num">([\s\S]*?)</i>'

    # 获取网页内容
    def __fetch_content(self):
        r = request.urlopen(Spider.url)
        htmls = r.read()
        htmls = str(htmls,encoding='utf-8')
        return htmls

    # 截取相应的数据，并以字典形式输出
    def __analysis(self, htmls):
        root_html = re.findall(Spider.root_pattern, htmls)

        anchors = []
        for html in root_html:
            name = re.findall(Spider.name_pattern, html)
            number = re.findall(Spider.number_pattern, html)
            anchor = {'name':name, 'number':number}
            anchors.append(anchor)
            
        return anchors
    
    # 数据处理(规范化)
    def __refine(self, anchors):
        l = lambda anchor:{
            'name':anchor['name'][0].strip(),
            'number':anchor['number'][0]
            }
        return map(l,anchors)

    # 数据排序
    def __sort(self, anchors):
        anchors = sorted(anchors, key=self.__sort_seed, reverse=True)
        return anchors
    
    # 数据排序规则
    def __sort_seed(self, anchor):
        r = re.findall('\d*',anchor['number'])
        number = float(r[0])
        if '万' in anchor['number']:
            number *= 10000
        return number
    
    # 数据输出
    def __show(self, anchors):
        print('————————————————————————————————')
        for rank in range(0, len(anchors)):
            print('No.' + str(rank + 1)
            +': '
            +anchors[rank]['name']
            +'  '
            +anchors[rank]['number'])
        print('————————————————————————————————')        

    # 调用私有方法的入口方法
    # 同时也是执行流程控制
    def go(self):
        htmls = self.__fetch_content()
        anchors = self.__analysis(htmls)
        anchors = list(self.__refine(anchors))
        anchors = self.__sort(anchors)
        self.__show(anchors)

spider = Spider()
spider.go()
