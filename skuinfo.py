# -*- coding:utf-8 -*-

import xlrd, openpyxl
import csv
import os

# 产品信息-产品SKU--类目#
fad = r"C:\Users\felix\Desktop\info"
filels = os.listdir(fad)
print filels
fad1 = fad + "\%s" % filels[0].decode("gbk")
print fad1
f1 = list(csv.reader(open(fad1)))
rown = len(f1)
cp_dict = {}
for row in f1:
    cp_dict[row[1]] = {"one": row[7].decode("gbk"), "two": row[9].decode("gbk"), "three": row[11].decode("gbk")}
# print cp_dict
print cp_dict["CA57BN"]["three"]

# 店铺sku信息--店铺sku--公司sku#

fad2 = fad + "\%s" % filels[1].decode("gbk")
print fad2
f2 = xlrd.open_workbook(fad2)
sheet_dpsku = f2.sheet_by_name("result")
rown1 = sheet_dpsku.nrows
print rown1
dpsku_dict = {}
for i in range(1, rown1):
    rowls = sheet_dpsku.row_values(i)
    # print rowls
    if rowls[6] == "ERROR":
        if "+" in rowls[2]:
            cpsku = rowls[2][:rowls[2].index("+")].strip()
        elif "PCS" in rowls[2].upper():
            try:
                cpsku = rowls[2][rowls[2].upper().index("PCS") + 4:rowls[2].upper().index("-")].strip()
            except ValueError as e1:
                cpsku = rowls[2][rowls[2].upper().index("PCS") + 4:rowls[2].upper().index("_")].strip()
        elif rowls[2][:2] in ["WT", "OT", "VP", "YP", "MY", "LV"]:
            cpsku = rowls[2][2:rowls[2].index("-")].strip()
        elif rowls[2][:4] == "VTVT":
            cpsku = rowls[2][2:rowls[2].index("-")].strip()
        else:
            cpsku = ""
    else:
        cpsku = rowls[6]
    dpsku_dict[rowls[1] + rowls[2]] = {"dpsku": rowls[2], "cpsku": cpsku, "ASIN": rowls[4]}
print dpsku_dict["AZVPUKPPC020BUK+PPC007BUS-TA"]
cpsku1 = dpsku_dict["AZVPUKPPC020BUK+PPC007BUS-TA"]["cpsku"]
print cp_dict[cpsku1]["three"]

#店铺类目负责人--店铺类目--负责人#
fad3 = fad + "\%s" % filels[2].decode("gbk")
print fad3
f3 = xlrd.open_workbook(fad3)
sheet_dplm = f3.sheet_by_name("result")
rown2 = sheet_dplm.nrows
print rown2
dplm_dict = {}
for j in range(1,rown2):
    rowls_lm=sheet_dplm.row_values(j)
    print rowls_lm[0]
    dplm_dict[rowls_lm[0]]={"dp":rowls_lm[2],"dplm":rowls_lm[3],"dpp":rowls_lm[4]}
print dplm_dict[u"AZVTDE台灯"]
