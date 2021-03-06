# coding=GBK

import urllib
import urllib2
import cookielib
import HTMLParser
import re
from __builtin__ import int
import smtplib, sys
from email.mime.text import MIMEText
from _ast import Sub
from __builtin__ import str


def init_cookie():
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    opener.addheaders = [('User-agent','Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)')]
    urllib2.install_opener(opener)


def query_step1():
    url_step1 = """https://www.airchina.sg/CAPortal/dyn/portal/doEnc"""

    para = {}
    para['SITE'] = 'B000CA00'
    para['LANGUAGE'] = 'GB'
    para['COUNTRY_SITE'] = 'SG'
    para['BOOKING_FLOW'] = 'REVENUE'
    para['TRIGGER_PAGE'] = 'SRCH'
    para['AIR_PARAM_PRICE_DISPLAY'] = 'ADT_TAX_FEE'
    para['langDateFormat'] = 'dd/MM/yyyy'
    para['IS_FLEXIBLE'] = 'TRUE'
    para['TRIP_TYPE'] = 'R'
    para['FSB1FromSource'] = 'Singapore, Changi International Airport  (SIN), Singapore'
    para['B_LOCATION_1'] = 'SIN'
    para['FSB1ToDestination'] = 'Weihai, Dashuibo Airport  (WEH), China'
    para['E_LOCATION_1'] = 'WEH'
    para['B_DATE_1'] = '30/01/2016'
    para['B_ANY_TIME_1'] = 'TRUE'
    para['B_DATE_2'] = '13/02/2016'
    para['B_ANY_TIME_2'] = 'TRUE'
    para['NB_ADT'] = '1'
    para['NB_CHD'] = '0'
    para['NB_INF'] = '0'
    para['CABIN'] = 'E'
    para['PROMO_CODE'] = ''

    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent }

    req = urllib2.Request(url_step1, urllib.urlencode(para), headers)
    content = urllib2.urlopen(req).read()
    return content

class Setp1Parser(HTMLParser.HTMLParser):
    def __init__(self):
        self.url = ''
        self.formData = {}
        self.inForm = False
        HTMLParser.HTMLParser.__init__(self)
        
    def handle_starttag(self, tag, attrs):
        if tag == 'form':
            self.inForm = True
            for name, value in attrs:
                if name == 'action':
                    self.url= 'https://www.airchina.sg' + value
        if tag == 'input' and self.inForm:
            tmpKey = ''
            for name, value in attrs:
                if name == 'name':
                    tmpKey = value
                if name == 'value':
                    self.formData[tmpKey] = value
            
                
                            
    def handle_data(self, data):
        pass
        
                            
    def handle_endtag(self, tag):
        if tag == 'form':
            self.inForm = False;


# <form accept-charset="utf-8" action="/CAOnline/dyn/air/booking/availability" method="post" name="redirectForm">
#     <input name="SITE" type="hidden" value="B000CA00"/>
#     <input name="LANGUAGE" type="hidden" value="GB"/>
#     <input name="COUNTRY_SITE" type="hidden" value="SG"/>
#     <input name="ENC" type="hidden" value="EF6CBA8CEF9271BB894E2A6F0D29245576394F7E7B50B60CA3E04E2C0F3C94EFD0366607E9EA06C054D8561091A8925B275E71561E23AAB9482DE78B5C46E50E5B540F0510890B95559B7393BA939512F0DB4DDCD2D34266511E317019377FA1F8E7CC4B2336E74A1EF528C671869927487F00ECB4C44E29BCFF4DD26157E32D14C1DDFD2B4B33A727D5B4FAF99AA7DB3EE3F7A40618DCCF230D3C90D3FE624A8176C33DBC52B71F0B6CB07835F3F6CDDB8A56DCB58F13055EF3E5EC7F2FDA00ACB6826A6E16A6A9048D8E4C9D3099237ACCABA794B301861ECD980468A248CB967358FC0CF82CAEFDB1CB6888B3056B969996FBA228716D179C59F33498CBA93B6179525F9B2670FAD0019472998B0A85FACA319DCA0637DF158222466BAF307EB6EBFDBE0863739900DAE3A8681BC11196A462CA1B6FFD3C7042E0DC45DCA847D7CAA6BFC3D2BBD88598978AD54A0D550DE88C44E419DF1D1565EAED4B102BC999E6C796A70C688890E4075A6C8FB40FCAA17FF82DA5761A8F43D5800D95FC620CFF9F73AEB7F55DA311A246166DCCC6F7B61910A35A082468FC8FB0582BE80F924931D5A8CD6F2F4DA252444633129188EB1344DB077B3ADC57083B7B466A3ADE94C8EE2FA72ED71CDEA5EF5766AD57C69D16A10FE69705471C84A26A56CBB27D638CCA1EE6B5501F5D0D855F07C7781F7631A605ABDB36F61B792713C78B4E1889B3604B590F82B401FF2B7C001D6A9090B7BA16F96E7F5940F9C97B12D998F9383309543416949FD54B6B41D0FEA066E7C01E805E954C3A5E3248064B6C524409A7644DBA3D41BB53B41E42A2BE3D8A618AAA71D6947DCD99E41EA2536A5EDDF1212042050AA0B3816FF98B8F7ED484DBEB73B8ECAADF956669FCDC216D"/>
#     <input name="ENCT" type="hidden" value="1"/>
# </form>
# 
#

class Setp2Parser(HTMLParser.HTMLParser):
    def __init__(self):
        self.url = ''
        self.current_number = ''
        self.find_lowest_data = False
        self.isNumber = False
        HTMLParser.HTMLParser.__init__(self)
        
    def handle_starttag(self, tag, attrs):
        if self.find_lowest_data:
            return
        if tag == 'span':
            for name, value in attrs:
                if value == 'sprite lowest-price-triangle':
                    self.find_lowest_data = True
                if value == 'number':
                    self.isNumber = True
                            
    def handle_data(self, data):
        if self.isNumber:
            self.current_number = data
            self.isNumber = False
        
                            
    def handle_endtag(self, tag):
        pass


def query_step2(url, formData):
    
    
    req = urllib2.Request(url, urllib.urlencode(formData));
    req.add_header("Referer", "https://www.airchina.sg/CAPortal/dyn/portal/doEnc")
    req.add_header("Origin", "https://www.airchina.sg")
    content = urllib2.urlopen(req).read()

    # fp = open("test.html", "w")
    # fp.write(content)
    # fp.close

    parserSetp2 = Setp2Parser()
    parserSetp2.feed(content)
    return parserSetp2.current_number

def send_email(dest_list, sub, content):

    mail_host = "smtp.126.com"
    mail_user = "derek_develop@126.com"
    mail_pass = "derek1986"
    
    me = mail_user + "<" + mail_user +  ">"
    msg = MIMEText(content, _charset="gbk")
    msg["Subject"] = sub
    msg["From"] = me
    msg["To"] = ";".join(dest_list)
    
    try:
        s = smtplib.SMTP()
        s.connect(mail_host)
        s.login(mail_user, mail_pass)
        s.sendmail(me, dest_list, msg.as_string())
        s.close()
        
        return True
    except Exception, e:
        print str(e)
        return False
    
def print_data(isPrint, data):
    if isPrint:
        print data

def sendmail(title, content):
    dest_list = ["keqi25@gmail.com"]
    if send_email(dest_list, title, content):
        return "send mail success"
    else :
        return "send mail failed"
    # print 'send email:' + title + ':' + content

def query_lowest(shreshold_price):
    title = ''
    content = ''
    isSendMail = False;
    try: 
        init_cookie()
        content = query_step1()
        parser_step1 = Setp1Parser()
        parser_step1.feed(content)
        result = query_step2(parser_step1.url, parser_step1.formData)
        title = u"new lowest price: " + result
        content = u"today lowest price is:" + result
        print u"lowest price:: " + result
        if float(result) < float(shreshold_price):
            isSendMail = True
    except Exception as e:
        isSendMail = True
        title = u"ticket error"
        content = str(e)
        print str(e)

    if isSendMail:
        return str(title) + "\n" + sendmail(title, content);
    else :
        return str(title) + "\n" + "Not send email"

def query_daily():
    title = ''
    content = ''
    try:
        init_cookie()
        content = query_step1()
        parser_step1 = Setp1Parser()
        parser_step1.feed(content)
        result = query_step2(parser_step1.url, parser_step1.formData)
        title = u"ticket price daily: " + result
        content = u"today lowest price is:" + result
        print u"ticket daily: " + result
    except Exception as e:
        title = u"ticket error"
        content = str(e)
        print str(e)

    return str(title) + "\n" + sendmail(title, content)


    
if __name__ == "__main__":
    query_result = query_daily()
    
