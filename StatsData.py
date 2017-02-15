#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2017-02-15 09:54:15
# @Author  : Nemo-Sailing
# @Link    : https://blog.ijita.me

import urllib2
import re

## 解析网页内容
def parseHTML(url):
    url_prefix = url[:(url.rfind("/") + 1)]
    # print(url)
    response = urllib2.urlopen(url)
    the_page = response.read()
    the_page_content = unicode(the_page,'GBK').encode('UTF-8')
    # print the_page_content
    regex = '<tr class=[^>]*tr[^>]*><td[^>]*?>(<a[^>]*>)?(\d+)(</a>)?</td>(<td>)?(\d+)?(</td>)?<td[^>]*?>(<a[^>]*>)?([^a]+)(</a>)?</td></tr>'
    pattern = re.compile(regex)
    data = pattern.finditer(the_page_content)
    return data, url_prefix

## 获取城市、区县、乡镇、村委会数据
def getData(url, data_prefix, level, max_level):
    '''
    Agrs:
    url - 国家统计局数据页面
    data_prefix - 数据前缀，用于拼数据行，初始时填空字符串
    level - 当前深度级别
    max_level - 最大深度级别
    '''
    data, url_prefix = parseHTML(url)
    for m in data:
        tp = m.groups()
        child_url = tp[0]
        child_data_prefix = data_prefix + tp[1] + ',' + tp[7]

        # 村委会级别有个特殊字段：城乡分类
        if tp[4] != None:
            child_data_prefix += "," + tp[4]

        # 不会超过一定的深度级别
        child_level = level + 1
        if child_level > max_level:
            print child_data_prefix
            continue

        if child_url != None:
            child_url = child_url[9:-2]
            child_data_prefix += ","
            getData(url_prefix + child_url, child_data_prefix, child_level, max_level)
        else:
            # 无下级页面了
            print child_data_prefix + ",,"

if __name__ == '__main__':
    base_url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2015/36.html'
    getData(base_url, "", 0, 2)
