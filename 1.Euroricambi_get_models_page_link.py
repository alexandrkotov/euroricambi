#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Парсинг ссылок на страницы моделей http://www.euroricambi.com

Использован Python 3.2.5 (32 bit)
pip установлен через get-pip.py
Selenium установлен через pip install -U selenium
'''
import os
import time
import urllib.request
import re
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from datetime import datetime


tStart = time.time()
globalCount = 0

link = "http://www.euroricambi.com/areariservata/Login.aspx"
user = "имя_пользователя"
password = "пароль"

reg_ex_family_index_html = re.compile(r'<a href=\"(.*?)\" title')
reg_ex_model_index_html = re.compile(r'<a href=\"(.*?)\" title')
reg_ex_model_name = re.compile(r'Model\">(.*?)<\/a>')

driver = Chrome()
driver.get(link)

#функция возвращет имя семейства по имени индексного html файла семейства
def get_family_name(index_html):

    if index_html == "indexL_WEB_REAR_AXLE.html":
        return "REAR AXLES SINGLE"
    elif index_html == "indexL_WEB_TANDEM.html":
        return "INTERMEDIATE TANDEM AXLE"
    else:
        return "не определено"    
    '''
    if index_html == "indexL_WEB_SINGLESINGLE.html":
        return "SINGLE AXLES SINGLE REDUCTION"
    elif index_html == "indexL_WEB_SINGLEDOUBLE.html":
        return "SINGLE AXLES DOUBLE REDUCTION"
    elif index_html == "indexL_WEB_TANDFORWSINGLE.html":
        return "TANDEM FORWARD AXLES SINGLE REDUCTION"
    elif index_html == "indexL_WEB_TANDREARSINGLE.html":
        return "TANDEM REAR AXLES SINGLE REDUCTION"
    elif index_html == "indexL_WEB_TANDFORWDOUBLE.html":
        return "TANDEM FORWARD AXLES DOUBLE REDUCTION"
    elif index_html == "indexL_WEB_TANDREARDOUBLE.html":
        return "TANDEM REAR AXLES DOUBLE REDUCTION"   
    else:
        return "не определено"
    '''
    '''
    if index_html == "indexL_WEB_SINGLEAXLE.html":
        return "REAR AXLE Single"
    elif index_html == "indexL_WEB_INTERMEDIO.html":
        return "INTERMEDIATE AXLE Tandem"
    elif index_html == "indexL_WEB_RAXLETANDEM.html":
        return "REAR AXLE Tandem"
    elif index_html == "indexL_WEB_HUBS.html":
        return "IVECO HUBS"
    else:
        return "не определено"

    '''
    '''
    if index_html == "indexL_WEB_GEARBOX.html":
        return "GEARBOX"
    
    else:
        return "не определено"
    '''
    '''
    if index_html == "indexL_WEB-AIR-CONTROLS.html":
        return "AIR CONTROLS"
    elif index_html == "indexL_WEB-REPAIR-KITS.html":
        return "REPAIR KITS"
    elif index_html == "indexL_WEB-INPUTSHAFT.html":
        return "INPUT SHAFTS SECTION"
    elif index_html == "indexL_WEB-HEAVYDUTY6S.html":
        return "HEAVY DUTY 6 SPEEDS"
    elif index_html == "indexL_WEB-HEAVYDUTY7S.html":
        return "HEAVY DUTY 7 SPEEDS"
    elif index_html == "indexL_WEB-HEAVYDUTY8S.html":
        return "HEAVY DUTY 8 SPEEDS"
    elif index_html == "indexL_WEB-HEAVYDUTY9S.html":
        return "HEAVY DUTY 9 SPEEDS"
    elif index_html == "indexL_WEB-HEAVYDUTY10S.html":
        return "HEAVY DUTY 10 SPEEDS"
    elif index_html == "indexL_WEB-HEAVYDUTY11S.html":
        return "HEAVY DUTY 11 SPEEDS"
    elif index_html == "indexL_WEB-HEAVYDUTY13S.html":
        return "HEAVY DUTY 13 SPEEDS"
    elif index_html == "indexL_WEB-HEAVYDUTY15S.html":
        return "HEAVY DUTY 15 SPEEDS"
    elif index_html == "indexL_WEB-HEAVYDUTY18S.html":
        return "HEAVY DUTY 18 SPEEDS"
    else:
        return "не определено"
    '''
    '''
    if index_html == "indexL_WEB_MIDRANGE5.html":
        return "MID RANGE 5 SPEEDS"
    elif index_html == "indexL_WEB_MIDRANGE6.html":
        return "MID RANGE 6 SPEEDS"
    elif index_html == "indexL_WEB_MIDRANGE9.html":
        return "MID RANGE 9 SPEEDS"
    elif index_html == "indexL_WEB_MIDRANGE16.html":
        return "MID RANGE 16 SPEEDS"
    elif index_html == "indexL_WEB_TWINSPLITTER.html":
        return "GEARBOX TWIN SPLITTER"
    else:
        return "не определено"
    '''
    '''
    if index_html == "indexLOGO_RASINGLE_WEB.html":
        return "REAR AXLE Single"
    elif index_html == "indexLOGO_SINGLE_TAN_WEB.html":
        return "REAR AXLE Single & Tandem"
    elif index_html == "indexLOGO_TANDEM_WEB.html":
        return "INTERMEDIATE AXLE Tandem"
    elif index_html == "indexLOGO_HUBS_WEB.html":
        return "REAR AND INTERMEDIATE AXLES HUBS"
    elif index_html == "indexPROP_SHAFT_WEB.html":
        return "PROPELLER SHAFT COMPONENTS"
    else:
        return "не определено"
    '''
    '''    
    if index_html == "indexL_WEBECOSPLIT1.html":
        return "ECOSPLIT I"
    elif index_html == "indexL_WEBECOSPLIT2.html":
        return "ECOSPLIT II"
    elif index_html == "indexL_WEBECOSPLIT3.html":
        return "ECOSPLIT III"
    elif index_html == "indexL_WEBNEWECOSPLIT.html":
        return "NEW ECOSPLIT"
    
    elif index_html == "indexL_WEBASTRONICLITE.html":
        return "AS Tronic lite (6 speeds)"
    elif index_html == "indexL_WEBASTRONICMIDTRUCK.html":
        return "AS Tronic mid Truck (12 speeds)"
    elif index_html == "indexL_WEBASTRUCK12SPEED.html":
        return "AS Tronic Truck (12 speeds)"
    elif index_html == "indexL_WEBASTRUCK16SPEED.html":
        return "AS Tronic Truck (16 speeds)"
    elif index_html == "indexL_WEBASTBUS10SPEED.html":
        return "AS Tronic Bus (10 speeds)"
    elif index_html == "indexL_WEBASTBUS12SPEED.html":
        return "AS Tronic Bus (12 speeds)"
    elif index_html == "indexL_WEBETRONIC6SPEED.html":
        return "eTronic (6 speeds)"

    elif index_html == "indexL_WEB12SPEED.html":
        return "ECOSPLIT IV (12 speeds)"
    elif index_html == "indexL_WEB16SPEED.html":
        return "ECOSPLIT IV (16 speeds)"
    elif index_html == "indexL_WEBSYNCHRONIZERKITS.html":
        return "SYNCHRONIZER KITS"
    elif index_html == "indexL_WEBSTEERINGPUMP.html":
        return "STEERING PUMP"
    elif index_html == "indexL_WEBPTO.html":
        return "P.T.O. (POWER TAKE OFF)"
    elif index_html == "indexL_WEBINTARDER.html":
        return "ECOSPLIT IV (12 speeds/16 speeds) INTARDER"

    elif index_html == "indexL_WEBECOLITE.html":
        return "ECOLITE"    
    elif index_html == "indexL_WEBNEWECOLITE.html":
        return "NEW ECOLITE"  
    elif index_html == "indexL_WEBECOMID.html":
        return "ECOMID"    
    elif index_html == "indexL_WEBNEWECOMID.html":
        return "NEW ECOMID"  


    #elif index_html == "":
    #    return ""

    elif index_html == "indexL_WEBGEARBOX-OLDGEN.html":
        return "GEARBOXES OLD GENERATION"
    
    elif index_html == "indexL_WEBGEARBOX-NEWGEN.html":
        return "GEARBOXES NEW GENERATION"

    #elif index_html == "":
    #    return ""
    #OLD
    elif index_html == "indexL_WEBFRONTAXLE.html":
        return "FRONT AXLE"

    elif index_html == "indexL_WEBINTERMEDIATEAXLE.html":
        return "INTERMEDIATE AXLE"

    elif index_html == "indexL_WEBHUBINTERAXLE.html":
        return "INTERMEDIATE AXLES HUB"

    elif index_html == "indexL_WEBREARAXLE.html":
        return "REAR AXLE"

    elif index_html == "indexL_WEBHUBREARAXLE.html":
        return "REAR AXLES HUB"

    elif index_html == "indexL_WEBTRANSFERCASE.html":
        return "TRANSFER CASE W600-3W"
    #NEW - полное совпадение с OLD, это номально
    #elif index_html == "indexL_WEBINTERMEDIATEAXLE.html":
    #    return "INTERMEDIATE AXLE"
    
    #elif index_html == "indexL_WEBHUBINTERAXLE.html":
    #    return "INTERMEDIATE AXLES HUB"

    #elif index_html == "indexL_WEBREARAXLE.html":
    #    return "REAR AXLE"

    #elif index_html == "indexL_WEBHUBREARAXLE.html":
    #    return "REAR AXLES HUB"

    #elif index_html == "":
    #    return ""



    
    else:
        return "не определено"
    '''

#функция возвращет массив имен семейств и их ссылок
def get_families_names_and_links(family_group_name, family_group_link):
    #webZF Transmissions
    family_group_doman = family_group_link.replace("index.html","")
    driver.get(family_group_link)
    #print("Группа семейств {} - успешно".format(family_group_name))
    time.sleep(1)
    #чтение ссылок семейств в рамках группы
    tbody_html = driver.find_element_by_tag_name('tbody').get_attribute('innerHTML')
    tbody_raw = tbody_html.split('<td class="images">')
    #print("Разрезок {}".format(len(tbody_raw)))
    res_arr = []
    for i in range(1,len(tbody_raw)):
        family_index_html = reg_ex_family_index_html.findall(tbody_raw[i])[0].strip()
        family_name = get_family_name(family_index_html)
        family_link = family_group_doman + family_index_html
        #print("{} - {}".format(family_name,family_link))
        res_str = family_name.strip() + ";" + family_link.strip()
        res_arr.append(res_str)
    return res_arr

#функция пишет в файл все модели в группе семейств
def get_all_model_link_in_family_group(family_group_name, family_group_link):
    f=open(fname,'a')
    families_names_and_links = []
    families_names_and_links.clear()
    families_names_and_links_arr = get_families_names_and_links(family_group_name, family_group_link)
    #print("\nМассив имен семейств и их ссылок {}\n".format(families_names_and_links_arr))
    print("\nВ группе семейств {}\n  найдено {} семейств:".format(family_group_name, len(families_names_and_links_arr)))
    time.sleep(2)
    for q in range(len(families_names_and_links_arr)):
        family_link = families_names_and_links_arr[q].split(';')[1]
        family_name = families_names_and_links_arr[q].split(';')[0]
        print("  {}".format(family_name))
        time.sleep(1)
        driver.get(family_link)

        model_grid_html = driver.find_element_by_id('tabella-prodotti').get_attribute('innerHTML')
        model_grid_raw = model_grid_html.split('<li>')

        for m in range(1,len(model_grid_raw)):
            model_index_html = reg_ex_model_index_html.findall(model_grid_raw[m])[0].strip()
            family_group_doman = family_group_link.replace("index.html","")
            model_link = family_group_doman + model_index_html
            model_name = reg_ex_model_name.findall(model_grid_raw[m])[0].strip().replace('\xd8','Diam.')
            #print("{} --- {} --- {}".format(family_name, model_name, model_link))
            res_str = family_group_name+";"+family_name+";"+model_name+";"+model_link+"\n"
            f.write(res_str)
    f.close()

#логинимся
driver.find_element_by_id('ctl00_cphAction_loginForm_UserName').send_keys(user)
driver.find_element_by_id('ctl00_cphAction_loginForm_Password').send_keys(password)
driver.find_element_by_name('ctl00$cphAction$loginForm$LoginButton').click()
print("Вход - успешно")
driver.find_element_by_link_text('Catalogues').click()
print("Переход в каталоги - успешно")

fname = "models_link.csv"
f=open(fname,'w')
f.close()

'''
family_group_name = "ZF Ecosplit I-II-III / New Ecosplit 12/3-4 - 2014"
family_group_link = "http://www.euroricambi.com/catalplus/95_02/index.html"
get_all_model_link_in_family_group(family_group_name, family_group_link)

family_group_name = "ZF AS Tronic and eTronic 12/6 - 2014"
family_group_link = "http://www.euroricambi.com/catalplus/95_05/index.html"
get_all_model_link_in_family_group(family_group_name, family_group_link)

family_group_name = "ZF Ecosplit IV 12/7 - 2015"
family_group_link = "http://www.euroricambi.com/catalplus/95_07/index.html"
get_all_model_link_in_family_group(family_group_name, family_group_link)

family_group_name = "ZF Ecolite - New Ecolite - Ecomid - New Ecomid 12/2 - 2015"
family_group_link = "http://www.euroricambi.com/catalplus/95_01/index.html"
get_all_model_link_in_family_group(family_group_name, family_group_link)
'''
'''
family_group_name = "MB Gearboxes 7/1 - Updated 2014"
family_group_link = "http://www.euroricambi.com/catalplus/60_03/index.html"
get_all_model_link_in_family_group(family_group_name, family_group_link)
'''
'''
family_group_name = "MB Differential Old Generation 7/2 - 2012"
family_group_link = "http://www.euroricambi.com/catalplus/60_02/index.html"
get_all_model_link_in_family_group(family_group_name, family_group_link)

family_group_name = "MB Differential New Generation 7/3 - 2012"
family_group_link = "http://www.euroricambi.com/catalplus/60_07/index.html"
get_all_model_link_in_family_group(family_group_name, family_group_link)
'''
'''
family_group_name = "MAN Differential 2016"
family_group_link = "http://www.euroricambi.com/catalplus/56_03/index.html"
get_all_model_link_in_family_group(family_group_name, family_group_link)
'''
'''
family_group_name = "FULLER Mid Range & Twin Splitter Updated 2014"
family_group_link = "http://www.euroricambi.com/catalplus/35_02/index.html"
get_all_model_link_in_family_group(family_group_name, family_group_link)
'''
'''
family_group_name = "IVECO Updated 2014"
family_group_link = "http://www.euroricambi.com/catalplus/30_01/index.html"
get_all_model_link_in_family_group(family_group_name, family_group_link)
'''
'''
family_group_name = "DANA (EATON AXLES) Updated 2014"
family_group_link = "http://www.euroricambi.com/catalplus/24_01/index.html"
get_all_model_link_in_family_group(family_group_name, family_group_link)
'''
family_group_name = "DAF 2012"
family_group_link = "http://www.euroricambi.com/catalplus/18_01/index.html"
get_all_model_link_in_family_group(family_group_name, family_group_link)



print("\nВремя выполнения: %f сек." % (time.time()-tStart))

