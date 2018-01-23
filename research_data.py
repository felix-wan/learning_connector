# -*- coding:utf-8 -*-
#适应全部国家的市调数据采集
#版本 V1
#-----------------------------------------------———需要导入的包—————————— -------------------—————#
import requests
import lxml.etree as etree
import random
import re
import wx
import time
import xlwt
import threading
import math
import socket
import xlrd
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#--------------------------------------获取User-Agent---------------------------------------------------------------#
def getagent():
    conts='''Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50
Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50
Mozilla/5.0 (Windows NT 5.2) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.122 Safari/534.30
Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)
Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.2; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)
Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11
Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 2.0.50727; .NET CLR 3.0.04506.648; .NET CLR 3.5.21022; .NET4.0E; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)
Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0'''
    agents=conts.split("\n")
    rr = random.randint(0, len(agents) - 1)
    agent = agents[rr].strip()
    return agent

#------------------------------读取解析页面，设置200秒超时后重新请求------------------------------------------------#
def getsoup(url):
    headers = {'User-Agent': getagent()
               }
    proxies = {
        'http': 'http://10.10.1.10:3128',
        'https': 'http://10.10.1.10:1080',
    }
    try:
        conts = requests.get(url, headers=headers, timeout=100)
        cont=conts.content
        code=conts.status_code
        html = etree.HTML(cont)
    except (requests.exceptions.ChunkedEncodingError ,requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout,requests.ConnectionError) as ss:
        try:
            text.AppendText(u"请求超时，让我们休息5秒吧！\n")
            time.sleep(5)
            conts = requests.get(url, headers=headers, timeout=50)
            cont = conts.content
            code = conts.status_code
            html = etree.HTML(cont)
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout,requests.ConnectionError) as sgd:
            text.AppendText(u"请求超时，跳过该链接！\n")
            time.sleep(1)
            code = 110
            html = "PASS"
    return [html,code]
#----------------------------    -----获取页面排名的函数，根据不同国家分三类----------------------------------------#
def getrank1(soup):
    rankls=[]
    try:
        dranks=soup.xpath('//*[@id="SalesRank"]/td[2]')[0].text.strip()
        if "." in dranks:
            drank = dranks.replace(".", "").replace("(", "")
        elif "," in dranks:
            drank = dranks.replace(",", "").replace("(", "")
        else:
            drank = dranks.replace("(", "")
    except IndexError as norad:
        try:
            dranks = etree.tostring(soup.xpath('//*[@id="SalesRank"]')[0])
            drank = re.findall(r'<b>Amazon.*?</b>(.*?)\(', dranks, re.S)[0].strip().replace("&amp;", "&")
            if "." in dranks:
                drank = drank.replace(".", "").replace("(", "")
            elif "," in dranks:
                drank = drank.replace(",", "").replace("(", "")
            else:
                drank = drank.replace("(", "")
        except IndexError as noran:
            drank = "no"
    rankls.append(drank)
    ranks=soup.xpath('//*[@class="zg_hrsr_item"]')
    for i in range(3):
        try:
            rank_num=ranks[i].xpath('span/text()')[0].strip()
            if "." in rank_num:
                rank_num = rank_num.replace(".", "")
            elif "," in rank_num:
                rank_num = rank_num.replace(",", "")
            rank_cont=ranks[i].xpath('span/a/text()')
            try:
                ssa=ranks[i].xpath('span/b/a/text()')[0]
                # print ssa
                rank_cont.append(ssa)
            except IndexError as dddds:
                rank_cont=rank_cont
            rank_cont=">".join(rank_cont)
        except IndexError as norank:
            rank_num="no"
            rank_cont="no"
        rankls.append(rank_num)
        rankls.append(rank_cont)
    return rankls
    # print ranls

def getrank3(soup):
    rankls=[]
    infos=soup.xpath('//table[@id="productDetails_detailBullets_sections1"]/tr')
    for info in infos:
        if "Rank" in info.xpath('th/text()')[0]:
            ranks=info.xpath('td/span/span')

            if "(" in ranks[0].xpath('text()')[0].strip():
                drank = ranks[0].xpath('text()')[0].strip().replace("(","")
            else:
                drank = "no"
            rankls.append(drank)
            for i in range(3):
                if drank == "no":
                    try:
                        rank = ranks[i]
                        rank_num = rank.xpath('text()')[0].strip()  # .split()[0]
                        rank_cont = ">".join(rank.xpath('a/text()'))
                    except IndexError as ass:
                        rank_num="no"
                        rank_cont="no"
                else:
                    try:
                        rank = ranks[i+1]
                        rank_num = rank.xpath('text()')[0].strip()  # .split()[0]
                        rank_cont = ">".join(rank.xpath('a/text()'))
                    except IndexError as assq:
                        rank_num="no"
                        rank_cont="no"

                rankls.append(rank_num)
                rankls.append(rank_cont)
        else:
            pass
    return rankls
#----------------------------------------获取上架时间函数，根据国家不同分三类---------------------------------------#
def time1(soup):
    timels = soup.xpath('//td[@class="bucket"]/div[@class="content"]/*/li')
    for times in timels:
        time = times.xpath('text()')[0].encode('utf-8')
        if re.search(r' [\d]{4}', str(time[-5:])):
            time11 = time
            return time11
        elif re.search(r'[\d]{4}/', str(time[:5])):
            time11 = time
            return time11

        else:
            pass
def timeus(soup):
    infos = soup.xpath('//table[@id="productDetails_detailBullets_sections1"]/tr')
    for info in infos:
        time3 = info.xpath('td/text()')[0].strip()
        if re.search(r' [\d]{4}', str(time3[-5:])):
            time = time3
            return time
        else:
            pass

def time2(soup):
    try:
        return soup.xpath('//tr[@class="date-first-available"]/td[2]/text()')[0].strip()
    except IndexError as notiems:
        return ""

def time3(soup):
    infos = soup.xpath('//table[@id="productDetails_detailBullets_sections1"]/tr|//table[@id="productDetails_db_sections"]/tr')
    for info in infos:
        if "Date" in info.xpath('th/text()')[0]:
            time = info.xpath('td/text()')[0].strip()
            return time
        else:
            pass

#总函数
def gettime(soup,country):
    if country=="US":
        try:
            time = time3(soup)
        except IndexError as qqw:
            time=gettime(soup)
    else:
        timel1=time1(soup)
        if timel1 is None:
            time = time2(soup)
        else:
            time=timel1
    return time
#--------------------------------获取页面要采集的页面信息，返回列表，主函数-----------------------------------------#
def getinfo(soup,ASIN,country):
    infols=[]
    try:
        brand =soup.xpath('//*[@id="brand"]/text()|//*[@id="bylineInfo"]/text()')[0].strip()
    except IndexError as nobrand:
        try:
            brands = soup.xpath('//*[@id="brand"]/@href|//*[@id="bylineInfo"]/@href')[0]
            brand = brands.split("=")[-1]
        except IndexError as bbsds:
            brand="no"
    infols.append(brand)
    try:
        RV_totals = soup.xpath('//*[@id="acrCustomerReviewText"]/text()')[0].encode('utf-8')
        if "," in RV_totals:
            RV_totals=RV_totals.replace(",","")
        elif ("." in RV_totals):
            RV_totals = RV_totals.replace(".", "")
        RV_total = re.findall(r'[\d]+', str(RV_totals))[0]
    except IndexError as noRV:
        RV_total = 0
    infols.append(RV_total)
    try:
        RV_avgs=soup.xpath('//*[@id="averageCustomerReviews"]/*/*[@id="acrPopover"]/@title')[0].encode('utf-8')
        RV_avg=re.findall(r'[\d]+\.[\d]*',str(RV_avgs))[0]
    except IndexError as noRV:
        RV_avg=0
    infols.append(RV_avg)
    try:
        prices=soup.xpath('//span[@id="priceblock_saleprice"]/text()|//span[@id="priceblock_ourprice"]/text()|//span[@id="priceblock_dealprice"]/text()|//*[@class_="priceLarge"]/text()')[0].encode('utf-8')
        # print prices
        if country=="JP":
            if prices[-4] ==",":
                prices = prices.replace(",", "")
                price = re.findall(r'[\d]+', str(prices))[0]
            else:
                price= re.findall(r'[\d]+', str(prices))[0]
        elif country in "USCAUKMX":
            if len(prices)>7:
                prices = prices.replace(",", "")
                price = re.findall(r'[\d]+\.*[\d]*', str(prices))[0]
            else:
                price = re.findall(r'[\d]+\.*[\d]*', str(prices))[0]
        else:
            if prices[-3] =="," and prices[-7] ==".":
                prices=prices.replace(".","")
                prices = prices.replace(",", ".")
                price=re.findall(r'[\d]+\.[\d]*',str(prices))[0]
            elif prices[-3] ==",":
                prices = prices.replace(",", ".")
                price = re.findall(r'[\d]+\.[\d]*', str(prices))[0]
    except IndexError as noprices:
        price="no"
    infols.append(price)
    # ----上架时间---#
    infols.append(gettime(soup,country))
    if country=="US":
        rankls = getrank3(soup)
        if rankls:
            rankls=rankls
        else:
            rankls=getrank1(soup)

    else:
        rankls=getrank1(soup)
    for j in range(len(rankls)):
        infols.append(rankls[j])
    try:
        title = soup.xpath('//*[@id="productTitle"]/text()|//*[@id="btAsinTitle"]/span/text()')[0].strip()
    except IndexError as shd:
        title = "no"

    infols.append(title)
    try:
        imglink=soup.xpath('//div[@id="imgTagWrapperId"]/img/@data-old-hires|//div[@id="imgTagWrapperId"]/img/@data-a-dynamic-image')[0]
        if imglink=="":
            imglinka=imglink=soup.xpath('//div[@id="imgTagWrapperId"]/img/@data-a-dynamic-image')[0]
            imglink=re.findall(r'"(.*?)"',str(imglinka))[0]
        else:
            imglink=imglink
    except IndexError as d_reason:
        img = etree.tostring(soup.xpath('//img[@id="main-image"]|//img[@id = "imgBlkFront"]')[0])
        Pimg = re.compile(r'src="(.*?)"')
        imglink = str(re.findall(Pimg, img)[0])
    infols.append(imglink)
    infols.append(str(imglink.split('/')[-1]).replace("%2B","+"))
    return [infols,imglink]
#-------------------------------------------------------获取表格行数-----------------------------------------#
def getnrow(t_name,m):
    data = xlrd.open_workbook(t_name)
    table = data.sheets()[m]
    nrows = table.nrows
    return nrows
#-----------------------图片写入网页---------------------------------#
def html(linkls,fname):
    # links=[]
    # for link in linkls:
    #     if len(link) >= 1:
    #         link = '<img src="%s">' % link
    #         links.append(link)
    #     else:
    #         pass
    cont = "\n".join(linkls).encode('utf-8')
    f = open("fzfile\%s.html"% fname, 'w')
    message = """
    <!doctype html>

    <html>
        <head>
            <!-- 字符编码集 -->
            <meta charset="utf-8" />
            <meta name="keywords" content="关键词，关键字" />
            <meta name="description" content="页面描述信息-80字以内描述信息" />
            <title>%s下载的图片</title>
            <style type="text/css">
                img {
                    height: 200px;
                    width: 200px;
                }
                td {
                    text-align:center
                }
            </style>
        </head>
    <body>
        <table border="1">
        <!-- caption元素可以生成表标题，其单元格列跨度为表格的列数 -->
        <caption><b> listing 采集结果</b> </caption>
        <tr>
            <!-- 可以使用rowspan和colspan来合并单元格 -->
            <th rowspan="1">首图</th>
            <th rowspan="1">ASIN</th>
            <th rowspan="1">Link</th>
            <th rowspan="1">品牌</th>
            <th rowspan="1">评论数</th>
            <th rowspan="1">评分</th>
            <th rowspan="1">价格</th>
            <th rowspan="1">上架时间</th>
            <th rowspan="1">大类排名</th>
            <th rowspan="1">小类排名1</th>
            <th rowspan="1">小类类目1</th>
            <th rowspan="1">小类排名2</th>
            <th rowspan="1">小类类目2</th>
            <th rowspan="1">小类排名3</th>
            <th rowspan="1">小类类目3</th>
            <th rowspan="1">Title</th>
            <th rowspan="1">img_link</th>
        </tr>
           %s

    </table>

    <a>导出表格</a>

    <script>
        // 使用outerHTML属性获取整个table元素的HTML代码（包括<table>标签），然后包装成一个完整的HTML文档，设置charset为urf-8以防止中文乱码
        var html = "<html><head><meta charset='utf-8' /></head><body>" + document.getElementsByTagName("table")[0].outerHTML + "</body></html>";
        // 实例化一个Blob对象，其构造函数的第一个参数是包含文件内容的数组，第二个参数是包含文件类型属性的对象
        var blob = new Blob([html], { type: "application/vnd.ms-excel" });
        var a = document.getElementsByTagName("a")[0];
        // 利用URL.createObjectURL()方法为a元素生成blob URL
        a.href = URL.createObjectURL(blob);
        // 设置文件名，目前只有Chrome和FireFox支持此属性
        a.download = "%s.xls";
    </script>

    </body>
    </html>""" % (str(fname), str(cont),str(fname))

    f.write(message)
    f.close()
#--------------------------------------------------------获取要采集的 ASIN------------------------------------------#
def getASIN():
    asin_ls=[]
    var=text.GetValue().encode('utf-8').strip().split('\n')
    for i in range(len(var)):
        if len(var[i])<=1:
            pass
        else:
            asin_ls.append(var[i])
    return asin_ls
#-------------------------------------HTML代码写入---------------------------------------------#
def writ_table(ls):
    codea='''
        <tr>
            <td width="100" height="100"><img src="%s" width="80" height="80" style="vertical-align:middle;"></td>
            <td width="100" height="100"> %s </td>
            <td width="100" height="100">%s</td>
            <td width="100" height="100">%s</td>
            <td width="100" height="100">%s</td>
            <td width="100" height="100">%s</td>
            <td width="100" height="100">%s</td>
            <td width="100" height="100">%s</td>
            <td width="100" height="100">%s</td>
            <td width="100" height="100">%s</td>
            <td width="100" height="100">%s</td>
            <td width="100" height="100">%s</td>
            <td width="100" height="100">%s</td>
            <td width="100" height="100">%s</td>
            <td width="100" height="100">%s</td>
            <td width="100" height="100">%s</td>
            <td width="100" height="100">%s</td>
        </tr>
    '''%(str(ls[15]),str(ls[0]),str(ls[1]),str(ls[2]),str(ls[3]),str(ls[4]),str(ls[5]),str(ls[6]),str(ls[7]),str(ls[8]),str(ls[9]),str(ls[10]),str(ls[11]),str(ls[12]),str(ls[13]),str(ls[14]),str(ls[15]))
    return codea
#--------------------------------------采集事件绑定函数-------------------------------------------------------------#
def start():
    country = cylist.GetStringSelection()
    if country in "JPUK":
        dlink="https://www.amazon.co.%s/dp/" % country.lower()
    else:
        if country=="US":
            dlink = "https://www.amazon.com/dp/"
        elif country =="MX":
            dlink = "https://www.amazon.com.mx/dp/"
        elif country =="AU":
            dlink = "https://www.amazon.com.au/dp/"
        else:
            dlink = "https://www.amazon.%s/dp/" % country.lower()
    file_name = e1.GetValue()
    asin_ls=getASIN()
    workbook = xlwt.Workbook(encoding='utf-8')
    sheet=workbook.add_sheet(u'采集结果', cell_overwrite_ok=True)
    col_name = ['ASIN', 'link', '品牌', '总评论数', '评分', '价格','上架时间', '大类排名', '小类排名1', '小类类目1', '小类排名2', '小类类目2', '小类排名3', '小类类目3', 'title','imglink','imgname']
    for mm in range(len(col_name)):
        sheet.write(0,mm,col_name[mm])
    text.Clear()
    text.AppendText(u'---------开始采集(共 %s 条)，大概需要一段时间请耐心等待！---------\n' % len(asin_ls))
    imgls=[]
    codels=[]
    for i in range(len(asin_ls)):
        ASIN = asin_ls[i].strip()
        url =dlink+ASIN
        t1=time.time()
        code=getsoup(url)[1]
        if code == 404:
            text.AppendText(u"------NO.%s %s 页面出错 !------ \n" % (i + 1, ASIN))
            continue
        elif code == 110:
            text.AppendText(u"------NO.%s %s 请求超时 !------ \n" % (i + 1, ASIN))
            continue
        else:
            soup = getsoup(url)[0]
            t2=time.time()
            text.AppendText(u"-%s-"% int(t2-t1))
            lss = getinfo(soup,ASIN,country)
            ls=lss[0]
            ls.insert(0,ASIN),ls.insert(1,url)
            # sheet.write(i+1, 0, ASIN)
            # sheet.write(i+1, 1, url)
            codes=writ_table(ls)
            codels.append(codes)
            for j in range(len(ls)):
                sheet.write(i+1, j, ls[j])
            workbook.save('fzfile\%s.xls' % file_name)
            imgls.append(lss[1])
            text.AppendText(u"------NO.%s %s 采集完毕 !------ \n" % (i + 1,ASIN))
        time.sleep(5)
        if i % 150 ==0 and i >0:
            print i
            time.sleep(300)
        else:
            continue
    # print codels
    html(codels,file_name)
    text.AppendText(u'---------全部采集完毕，可以关闭此窗口!----------')
    wx.MessageBox(u'全部采集完毕，可以关闭此窗口!^~^', u'提示', wx.OK | wx.CANCEL, mb)

#-----------------------------------------验证IP函数---------------------------------------------------------#
def yz():

    localIP = socket.gethostbyname(socket.gethostname())
    IP = localIP[:10]
    IP="192.168.65"
    if IP in ['192.168.65','192.168.10','192.168.20','192.168.69','192.168.63',
          '192.168.72','192.168.55','192.168.75','192.168.30','192.168.20','192.168.45']:
        zyjj="OK"
    else:
        wx.MessageBox(u'你没有权限使用，请于管理员联系！', u'提示', wx.OK | wx.CANCEL, mb)
        time.sleep(2)
        win.Destroy()
        exit()
    return zyjj
#--------------------------------------------查询事件绑定函数--------------------  ---------------------------------#
def getcx():
    country = cylist.GetStringSelection()
    if country in "JPUK":
        dlink = "https://www.amazon.co.%s" % country.lower()
    else:
        if country == "US":
            dlink = "https://www.amazon.com"
        elif country =="MX":
            dlink = "https://www.amazon.com.mx"
        elif country =="AU":
            dlink = "https://www.amazon.com.au"
        else:
            dlink = "https://www.amazon.%s" % country.lower()
    word=e1.GetValue()
    N=e2.GetValue()
    if N=="N":
        num=20
    else:
        num=int(N)
    page=int(math.ceil(num/25.0))+1
    print page
    text.Clear()
    text.AppendText(u'开始采集（共%s个）\n' % (num))
    ls = []
    for m in range(page):
        url = dlink+"/s/page=%s&keywords=%s" %(m+1,word)
        headers = {'User-Agent': getagent()
                   }
        try:
            conts = requests.get(url, headers=headers, timeout=200).content
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout) as ss:
            text.AppendText(u"请求超时，让我们休息5秒吧！")
            time.sleep(5)
            conts = requests.get(url, headers=headers, timeout=200).content
        except requests.ConnectionError as sgd:
            text.AppendText(u"请求超时，让我们休息5秒吧！")
            time.sleep(5)
            conts = requests.get(url, headers=headers, timeout=200).content
        html = etree.HTML(conts)
        info = html.xpath('//li[contains(@id,\'result_\')]')
        for lils in info:
            gg = lils.xpath('div/div/div/div[2]/h5/text()')
            asin = lils.xpath('@data-asin')[0]
            if len(gg) >= 1:
                pass
            else:
                ls.append(asin)
    for j in range(num):
        text.AppendText(u'%s\n'% ls[j])
#------------------------------------------采集和查询进程-----------------------------------------------------------#

#采集进程
def xc(even):
    country = cylist.GetStringSelection().encode('utf-8')
    if country == "":
        wx.MessageBox(u'请选择/输入国家简称（输入完后重新点击开始）', u'提示', wx.OK | wx.CANCEL, mb)
    else:
        zyjj = yz()
        if zyjj == "OK":
            th = threading.Thread(target=start)
            th.start()
        else:
            win.Destroy()

#查询进程
def cx(even):
    country = cylist.GetStringSelection().encode('utf-8')
    if country == "":
        wx.MessageBox(u'请选择/输入国家简称（输入完后重新点击开始）', u'提示', wx.OK | wx.CANCEL, mb)
    else:
        zyjj = yz()
        if zyjj == "OK":
            th = threading.Thread(target=getcx)
            th.start()
        else:
            win.Destroy()

def qut(even):
    win.Destroy()
#-------------------------------------GUI窗口编辑模块--------------------------------------------------------------#
app=wx.App()
win=wx.Frame(None,wx.ID_ANY,title=u"市调数据采集器",size=(520,600))
mb=wx.Panel(win,-1)
font = wx.Font(12, wx.DECORATIVE,wx.NORMAL, wx.NORMAL)
font1 = wx.Font(11, wx.DECORATIVE,wx.ITALIC, wx.NORMAL)
e1=wx.TextCtrl(mb,-1,u'请输入文件名/查询词',pos=(15,15),size=(150,-1))
bt=wx.Button(mb,label=u"采集",pos=(200,10),size=(100,30))
btc=wx.Button(mb,label=u"查询",pos=[290,10],size=(100,30))
btq=wx.Button(mb,label=u"退出",pos=[380,10],size=(100,30))
ctylist=[u'DE',u'ES',u'FR',u'IT',u'UK',u'CA',u'JP',u'US',u'MX',u'AU']
cylist=wx.ComboBox(mb,-1,pos=(20,50),choices=ctylist,size=(100,30))
e2=wx.TextCtrl(mb,-1,u'N',pos=(40,50))
lb1=wx.StaticText(mb,-1,u"备注：请根据需求选择/输入国家简称(大写)：",pos=(300,50))
text=wx.TextCtrl(mb,-1,pos=(15,100),size=(460,350),style=wx.TE_MULTILINE|wx.TE_RICH)
e1.SetFont(font1)
lb1.SetFont(font)
bt.Bind(wx.EVT_BUTTON,xc,None,-1,-1)
btc.Bind(wx.EVT_BUTTON,cx,None,-1,-1)
btq.Bind(wx.EVT_BUTTON,qut,None,-1,-1)
xbox=wx.BoxSizer()
xbox.Add(e1,proportion=1,flag=wx.EXPAND)
xbox.Add(bt,proportion=0,flag=wx.RIGHT)
xbox.Add(btc,proportion=0,flag=wx.RIGHT)
xbox.Add(btq,proportion=0,flag=wx.RIGHT)
x1box=wx.BoxSizer()
x1box.Add(lb1,proportion=0.7,flag=wx.RIGHT)
x1box.Add(cylist,proportion=0.2,flag=wx.RIGHT)
x1box.Add(e2,proportion=0.1,flag=wx.RIGHT)
ybox=wx.BoxSizer(wx.VERTICAL)
ybox.Add(xbox,proportion=0,flag=wx.EXPAND|wx.ALL,border=10)
ybox.Add(x1box,proportion=0,flag=wx.EXPAND|wx.ALL,border=5)
ybox.Add(text,proportion=1,flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM)
mb.SetSizer(ybox)
win.Show()
app.MainLoop()
