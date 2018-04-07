#!/usr/bin/python3
# -*- coding: utf-8 -*-
'''
Получение комплекта заготовок для модели по готовым линкам 
http://www.euroricambi.com

Время выполнения: 7505.195714 сек. для 451 модели КПП

Использован Python 3.2.5 (32 bit)
pip установлен через get-pip.py
Selenium установлен через pip install -U selenium
'''
import os
from os import listdir
import time
import urllib.request
import re
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from datetime import datetime

reg_ex_logo = re.compile(r'<img src=\"(.*?)\" class=\"vcentro')
reg_ex_titolo = re.compile(r'<img border=\".\" src=\"(.*?)\" alt=\"\">')
reg_ex_gruppo = re.compile(r'<img border=\".\" src=\"(.*?)\" width=\"')
reg_ex_header = re.compile(r'<font size=\".\">(.*?)<\/font')
reg_ex_fig = re.compile(r'\;">(.*?)<\/a>')
reg_ex_value = re.compile(r'\">(.*?)<\/td>')
reg_ex_notes_full = re.compile(r"overlib.\'(.*?)\',")
reg_ex_notes_short = re.compile(r';\">(.*?)<\/a')


#функция входа на сайт Euroricambi
def login(link, user, password, driver):
    driver.get(link)
    #логинимся
    driver.find_element_by_id('ctl00_cphAction_loginForm_UserName').send_keys(user)
    driver.find_element_by_id('ctl00_cphAction_loginForm_Password').send_keys(password)
    driver.find_element_by_name('ctl00$cphAction$loginForm$LoginButton').click()
    print("Вход - успешно")
    driver.find_element_by_link_text('Catalogues').click()
    print("Переход в каталоги - успешно")

#функция проверки порядка и типа полей по заголовку в all_raw[0]
def check_header(header):#all_raw[0]
    header_row_raw = header.split('<td class')
    Fig = None
    OurNo = None
    PartNo = None
    Description = None
    Notes = None
    Qty = None
    TP = None
    try:
        Fig = reg_ex_header.findall(header_row_raw[1])[0]
        OurNo = reg_ex_header.findall(header_row_raw[2])[0]
        PartNo = reg_ex_header.findall(header_row_raw[3])[0]
        Description = reg_ex_header.findall(header_row_raw[5])[0]
        Notes = reg_ex_header.findall(header_row_raw[6])[0]
        Qty = reg_ex_header.findall(header_row_raw[7])[0]
        TP = reg_ex_header.findall(header_row_raw[8])[0]

        if Fig == "Fig." and OurNo == "Our No." and PartNo == "Part No." and Description == "Description" and Notes == "Notes" and Qty == "Q.ty" and TP == "TP":
            print("Порядок и тип полей - проверено")
            return True
        else:
            print("Тип полей - Ok, порядок полей - ошибка")
            return False   
    except:
        print("Порядок или тип полей нестандартные")
        return False

#функция возвращает подготовленную строку
def get_row(cur_row_raw, count_flag_col):

    res_str = ""
    #разбираем строку, сначала по стандартным полям
    cur_row_raw = cur_row_raw.split('<td class')

    Fig = reg_ex_fig.findall(cur_row_raw[1])[0].strip()
    OurNo = reg_ex_value.findall(cur_row_raw[2])[0].strip()
    PartNo = reg_ex_value.findall(cur_row_raw[3])[0].strip()
    Description = reg_ex_value.findall(cur_row_raw[5])[0].replace(";",",").strip()
    Notes_full = ""
    try:
        Notes_full = reg_ex_notes_full.findall(cur_row_raw[6])[0].replace(";",",").strip()
    except:
        Notes_full = ""
    Notes_short = ""
    try:
        Notes_short = reg_ex_notes_short.findall(cur_row_raw[6])[0].replace("<br>","").replace(";",",").strip()
    except:
        Notes_short = ""
    Qty = reg_ex_value.findall(cur_row_raw[7])[0].strip()
    TP = ""
    try:
        TP = reg_ex_value.findall(cur_row_raw[8])[0].replace("<br>","").replace(";",",").strip()
        if TP.find("overlib") > -1:
            TP = reg_ex_notes_full.findall(cur_row_raw[8])[0].replace("<br>","").replace(";",",").strip()
    except:
        TP = reg_ex_notes_full.findall(cur_row_raw[8])[0].replace("<br>","").replace(";",",").strip()

    res_str = Fig+";"+OurNo+";"+PartNo+";"+Description+";"+Notes_full+";"+Notes_short+";"+Qty+";"+TP
    #теперь в цикле по полям с флажками
    for cell_index in range(1,count_flag_col+1):
        cell_box = ""
        cell_gruppo = ""
        if cur_row_raw[cell_index+8].find("box.jpg") > -1:
            cell_box = "*"
            cell_gruppo = reg_ex_notes_full.findall(cur_row_raw[cell_index+8])[0].strip()
            res_str = res_str +";"+ cell_box + ";" + cell_gruppo
        else:
            res_str = res_str + ";;"
    res_str = res_str + "\n"
    return res_str

#функция создания одного набора
def get_kit(kitNumber,family_group_name,family_name,model_name,model_link):

    dirKit = os.path.join(r'kit')
    kit_folder_name = str(kitNumber + 100000)[1:].strip()
    dirKitFolder = dirKit + "\\" + kit_folder_name

    if not os.path.exists(dirKitFolder):  
        os.makedirs(dirKitFolder)

    driver.get(model_link)
    print('Переход на страницу модели "{}" - успешно'.format(model_name))
    time.sleep(0.3)
    #Общий Notes по модели
    model_notes_link = model_link.replace("index","note")
    driver.get(model_notes_link)
    notes_text = driver.find_elements_by_class_name('piccolo')[0].text.replace('\xe7','c').replace('\xa3','L').replace('\xd8','Diam.')
    notes_file = os.path.join(dirKitFolder, 'notes.txt')
    fnotes=open(notes_file,'w')
    fnotes.write(notes_text)
    fnotes.close()
    print("Notes - скопирован")
    time.sleep(0.3)
    driver.get(model_link)
    model_domen = model_link.replace("index.htm","")

    #копируем большую схему и схему для печати
    tavola9 = model_domen + "tavola9.jpg"
    pic_tavola9 = os.path.join(dirKitFolder, 'tavola9.jpg')

    tavola_print = model_domen + "tavola_print.jpg"
    pic_tavola_print = os.path.join(dirKitFolder, 'tavola_print.jpg')

    urllib.request.urlretrieve(tavola9, pic_tavola9)
    print("tavola9.jpg - скопирован")
    urllib.request.urlretrieve(tavola_print, pic_tavola_print)
    print("tavola_print.jpg - скопирован")
    time.sleep(0.8)

    #карта ссылок!!!
    driver.switch_to_frame('leftFrame')
    z100=driver.find_elements_by_partial_link_text('100%')[0]
    z100.click()
    map_html = driver.find_element_by_id('immagine').get_attribute('innerHTML')
    map_file = os.path.join(dirKitFolder, 'raw_map.txt')
    fmap=open(map_file,'w')
    fmap.write(map_html)
    fmap.close()
    print("Карта ссылок выгружена в файл raw_map.txt")
    time.sleep(0.8)

    #переходим во фрейм с картинкой, чтобы вытянуть LOGO
    driver.get(model_domen + "tavola4.htm")
 
    url_raw = model_domen.split("/")
    logo_pref_url = "http://www.euroricambi.com/"+url_raw[3]+"/"+url_raw[4]+"/"
    try:
        logo_html = driver.find_elements_by_class_name('intestazione')[0].get_attribute('innerHTML')
        logo = logo_pref_url + reg_ex_logo.findall(logo_html)[0][3:]
        pic_logo = os.path.join(dirKitFolder, 'LOGO.jpg')
        urllib.request.urlretrieve(logo, pic_logo)
        print("LOGO.jpg - скопирован")
    except:
        time.sleep(2)
        try:
            logo_html = driver.find_elements_by_class_name('intestazione')[0].get_attribute('innerHTML')
            logo = logo_pref_url + reg_ex_logo.findall(logo_html)[0][3:]
            pic_logo = os.path.join(dirKitFolder, 'LOGO.jpg')
            urllib.request.urlretrieve(logo, pic_logo)
            print("LOGO.jpg - скопирован со второй попытки")
        except:
            print("LOGO.jpg - ОШИБКА копирования после двух попыток")
    time.sleep(0.9)
    
    #переходим во фрейм с таблицей
    driver.get(model_domen + "catalogo.htm")
    all_html = driver.find_element_by_tag_name('html').get_attribute('innerHTML') 
    titolo_pref_url = logo_pref_url
    try:    
        titolo = titolo_pref_url + reg_ex_titolo.findall(all_html)[0][3:]
        pic_titolo = os.path.join(dirKitFolder, 'TITOLOGRAF.jpg')
        urllib.request.urlretrieve(titolo, pic_titolo)
        print("TITOLOGRAF.jpg - скопирован")
    except:
        time.sleep(2)
        try:
            titolo = titolo_pref_url + reg_ex_titolo.findall(all_html)[0][3:]
            pic_titolo = os.path.join(dirKitFolder, 'TITOLOGRAF.jpg')
            urllib.request.urlretrieve(titolo, pic_titolo)
            print("TITOLOGRAF.jpg - скопирован со второй попытки")
        except:
            print("TITOLOGRAF - ОШИБКА копирования после двух попыток")
    time.sleep(0.9)
    
    #подсчёт количества gruppoXXXX.png и скопирование
    gruppo_raw = reg_ex_gruppo.findall(all_html)

    for g in range(len(gruppo_raw)):
        cur_link = model_domen + gruppo_raw[g]
        try:
            pic_gruppo = os.path.join(dirKitFolder, gruppo_raw[g])
            time.sleep(0.8)
            urllib.request.urlretrieve(cur_link, pic_gruppo)
            print("{} - скопирован".format(gruppo_raw[g]))
        except:
            try:
                pic_gruppo = os.path.join(dirKitFolder, gruppo_raw[g])
                time.sleep(2)
                urllib.request.urlretrieve(cur_link, pic_gruppo)
                print("{} - скопирован со второй попытки".format(gruppo_raw[g]))
            except:
                try:
                    pic_gruppo = os.path.join(dirKitFolder, gruppo_raw[g])
                    time.sleep(5)
                    urllib.request.urlretrieve(cur_link, pic_gruppo)
                    print("{} - скопирован с третьей попытки".format(gruppo_raw[g]))
                except:
                    print("{} - ОШИБКА копирования после трёх попыток".format(gruppo_raw[g]))
        

    #режем all_html на строки по <tr>
    all_raw = all_html.split('<tr class')
    print("Строк с данными {}".format(len(all_raw)-1))

    if check_header(all_raw[0]) == False:
        print("Ошибка заголовков, работа скрипта прекращена")
        quit()

    count_flag_col = len(all_raw[0].split('<td class'))-9
    print("Столбцов с флажками {}".format(str(count_flag_col)))

    fname = os.path.join(dirKitFolder, 'table.csv')
    f=open(fname,'w')
    for i in range(1,len(all_raw)):
        res_str = get_row(all_raw[i],count_flag_col).replace('\xe7','c').replace('\xa3','L').replace('\xd8','Diam.')
        f.write(res_str) 
    f.close()
    print("Таблица выгружена в файл table.csv")

#главная функция создания наборов
def get_models_kit(lastkitNumber):

    dirKit = os.path.join(r'kit')
    if not os.path.exists(dirKit):  
        os.makedirs(dirKit)

    kitNumber = 0
    #family_group_name = "ZF Ecolite - New Ecolite - Ecomid - New Ecomid 12/2 - 2015"
    #family_name = "NEW ECOMID"
    #model_name = "1324 - 9S 1310 TO"
    #model_link = "http://www.euroricambi.com/catalplus/95_01/165/index.htm"

    #читаем аргументы из models_link.csv для функции get_kit

    fl=open('models_link.csv','r')
    for line in fl:
        kitNumber = kitNumber + 1
        l = line.split(";")
        family_group_name = l[0].strip()
        family_name = l[1].strip()
        model_name = l[2].strip()
        model_link = l[3].strip()
        print('\n{} - "{}"'.format(str(kitNumber),model_name))
        #если был сбой, то продолжить с последнего успешного kit
        #если все kit скачены, то выставить номер последнего, чтобы дальше запустилась проверка
        if kitNumber > lastkitNumber:#0:#== 426:#> 450:
            try:
                get_kit(kitNumber,family_group_name,family_name,model_name,model_link)
            except:
                time.sleep(2)
                try:
                    get_kit(kitNumber,family_group_name,family_name,model_name,model_link)
                except:
                    try:
                        time.sleep(5)
                        get_kit(kitNumber,family_group_name,family_name,model_name,model_link)
                    except:
                        lastkitNumber = kitNumber - 1
                        return lastkitNumber
    fl.close()
    return 0


#функция повторного создания определенного набора
def repair_kit(repairKitNumber):

    dirKit = os.path.join(r'kit')
    kitNumber = 0
    fl=open('models_link.csv','r')
    for line in fl:
        kitNumber = kitNumber + 1
        l = line.split(";")
        family_group_name = l[0].strip()
        family_name = l[1].strip()
        model_name = l[2].strip()
        model_link = l[3].strip()
        
        if kitNumber == repairKitNumber:
            try:
                get_kit(kitNumber,family_group_name,family_name,model_name,model_link)
                print('\n{} - "{} - ВОССТАНОВЛЕН"'.format(str(kitNumber),model_name))
            except:
                time.sleep(2)
                try:
                    get_kit(kitNumber,family_group_name,family_name,model_name,model_link)
                    print('\n{} - "{} - ВОССТАНОВЛЕН со второй попытки"'.format(str(kitNumber),model_name))
                except:
                    print("В скрипте выставь параметр = номеру последнего набора и перезапусти скрипт")
                    quit()
    fl.close()

#функция проверки полноты наборов
#в каждом наборе обязательно должны быть:
#gruppo1.png - gruppo12.png, tavola9.jpg, tavola_print.jpg, raw_map.txt, notes.txt, table.csv
def check_kits():

    break_kit_arr = []
    dirKit = os.path.join(r'kit')
    q = listdir("./kit")
    #print(q)
    for i in range(len(q)):
        dirKitFolder = dirKit + "\\" + q[i]
        kit_number = int(q[i])
        #print("dirKitFolder = {}, kit_number = {}".format(dirKitFolder,str(kit_number)))
        gruppo1 = dirKitFolder + "\\gruppo1.png"
        if not os.path.exists(gruppo1):
            print("в {} нет {}".format(dirKitFolder,gruppo1))
            break_kit_arr.append(kit_number)

        gruppo2 = dirKitFolder + "\\gruppo2.png"
        if not os.path.exists(gruppo2):
            print("в {} нет {}".format(dirKitFolder,gruppo2))
            break_kit_arr.append(kit_number)

        gruppo3 = dirKitFolder + "\\gruppo3.png"
        if not os.path.exists(gruppo3):
            print("в {} нет {}".format(dirKitFolder,gruppo3))
            break_kit_arr.append(kit_number)

        gruppo4 = dirKitFolder + "\\gruppo4.png"
        if not os.path.exists(gruppo4):
            print("в {} нет {}".format(dirKitFolder,gruppo4))
            break_kit_arr.append(kit_number)

        gruppo5 = dirKitFolder + "\\gruppo5.png"
        if not os.path.exists(gruppo5):
            print("в {} нет {}".format(dirKitFolder,gruppo5))
            break_kit_arr.append(kit_number)

        gruppo6 = dirKitFolder + "\\gruppo6.png"
        if not os.path.exists(gruppo6):
            print("в {} нет {}".format(dirKitFolder,gruppo6))
            break_kit_arr.append(kit_number)

        gruppo7 = dirKitFolder + "\\gruppo7.png"
        if not os.path.exists(gruppo7):
            print("в {} нет {}".format(dirKitFolder,gruppo7))
            break_kit_arr.append(kit_number)

        gruppo8 = dirKitFolder + "\\gruppo8.png"
        if not os.path.exists(gruppo8):
            print("в {} нет {}".format(dirKitFolder,gruppo8))
            break_kit_arr.append(kit_number)

        gruppo9 = dirKitFolder + "\\gruppo9.png"
        if not os.path.exists(gruppo9):
            print("в {} нет {}".format(dirKitFolder,gruppo9))
            break_kit_arr.append(kit_number)

        gruppo10 = dirKitFolder + "\\gruppo10.png"
        if not os.path.exists(gruppo10):
            print("в {} нет {}".format(dirKitFolder,gruppo10))
            break_kit_arr.append(kit_number)

        gruppo11 = dirKitFolder + "\\gruppo11.png"
        if not os.path.exists(gruppo11):
            print("в {} нет {}".format(dirKitFolder,gruppo11))
            break_kit_arr.append(kit_number)

        gruppo12 = dirKitFolder + "\\gruppo12.png"
        if not os.path.exists(gruppo12):
            print("в {} нет {}".format(dirKitFolder,gruppo12))
            break_kit_arr.append(kit_number)

        tavola9 = dirKitFolder + "\\tavola9.jpg"
        if not os.path.exists(tavola9):
            print("в {} нет {}".format(dirKitFolder,tavola9))
            break_kit_arr.append(kit_number)

        tavola_print = dirKitFolder + "\\tavola_print.jpg"
        if not os.path.exists(tavola_print):
            print("в {} нет {}".format(dirKitFolder,tavola_print))
            break_kit_arr.append(kit_number)

        raw_map = dirKitFolder + "\\raw_map.txt"
        if not os.path.exists(raw_map):
            print("в {} нет {}".format(dirKitFolder,raw_map))
            break_kit_arr.append(kit_number)

        notes = dirKitFolder + "\\notes.txt"
        if not os.path.exists(notes):
            print("в {} нет {}".format(dirKitFolder,notes))
            break_kit_arr.append(kit_number)

        table = dirKitFolder + "\\table.csv"
        if not os.path.exists(table):
            print("в {} нет {}".format(dirKitFolder,table))
            break_kit_arr.append(kit_number)

    tmp_set = set(break_kit_arr)
    break_kit_arr = list(tmp_set)
    break_kit_arr.sort()
    #print(break_kit_arr)
    return break_kit_arr

#обёртка для функций проверки и починки наборов
def check_and_repair_kit():
    
    break_kit_arr = check_kits()
    while len(break_kit_arr) > 0:
        for k in range(len(break_kit_arr)):
            repair_kit(break_kit_arr[k])
        break_kit_arr=check_kits()

    if len(break_kit_arr) == 0:
        print("Проверка наборов завершена")
    else:
        print("Неполные наборы {}".format(str(break_kit_arr)))


########################################################################################
tStart = time.time()
globalCount = 0




link = "http://www.euroricambi.com/areariservata/Login.aspx"
user = "имя_пользователя"
password = "пароль"

driver = Chrome()
login(link, user, password, driver)
lastkitNumber = get_models_kit(0)#0 - старт, от 0 до макс. номера - продолжение, больше макс. номера - проверка и докачка 

#автоматический перезапуск
if lastkitNumber > 0:
    driver.close()
    time.sleep(4)
    print("\n\n==== ПОВТОРНЫЙ ЗАПУСК ПОСЛЕ ПЕРВОГО ОТКАЗА В ОБСЛУЖИВАНИИ СО СТОРОНЫ САЙТА EURORICAMBI ====\n\n")
    driver = Chrome()
    login(link, user, password, driver)
    if get_models_kit(lastkitNumber) == 0:
        check_and_repair_kit()
    else:
        print("Повторный отказ в обслуживании со стороны сайта Euroricambi")
        print("В скрипте выставь параметр = номеру последнего успешного набора и перезапусти скрипт")
        quit()

else:
    check_and_repair_kit()





print("\nВремя выполнения: %f сек." % (time.time()-tStart))



