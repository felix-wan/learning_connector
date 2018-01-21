# -*- coding:utf-8 -*-
# 数据中心工具的自动化测试
#http://bluemars.applinzi.com
# --------支持的包---------#
import chardet
import time
from openpyxl import Workbook
from selenium import webdriver
import lxml.etree as etree
from selenium.webdriver.common.keys import Keys
import xlrd
import requests

dv = webdriver.Chrome()
# 登陆账号#
dv.get("https://tool.patozon.net/p/login.php?from=bi")
time.sleep(2)
user = dv.find_element_by_name("user")
user.send_keys("felix")
pw = dv.find_element_by_name("pass")
pw.send_keys("!@##@!")
pw.submit()
time.sleep(2)
# -------------------------------点击进入销售参谋#
sscm = dv.find_element_by_link_text(u"销售参谋")
sscm.click()
time.sleep(3)

# 跳转页面#
windows = dv.window_handles
dv.switch_to.window(windows[-1])
time.sleep(2)

#选择店铺--先点击(第一部分)再选择店铺（四部-账号-国家）#
dp_select = dv.find_element_by_class_name("shop-name")
dp_select.click()
time.sleep(1)
#获取店铺列表
code = dv.page_source
html = etree.HTML(code)
dpls = html.xpath('//*[@class="btn-group selectShop open"]/ul/li')
dplsz=[]
for dp in dpls:
    try:
        dpz=dp.xpath('a/text()')[0]
        dplsz.append(dpz)

    except IndexError as e1:
        pass
print dplsz
#选取店铺
dp_input = dv.find_element_by_link_text("四部-VT-US")
dp_input.click()
time.sleep(1)

#库存管理模块#
kc_select = dv.find_element_by_partial_link_text("库存管理")
kc_select.click()
time.sleep(1)
kc = dv.find_element_by_partial_link_text("库存列表")
kc.click()
time.sleep(1)

#点击下载按钮#
download_bt=dv.find_element_by_id("exportXls")
download_bt.click()
time.sleep(1)

