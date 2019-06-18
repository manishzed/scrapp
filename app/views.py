
from django.shortcuts import render

# Create your views here.
       
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup 
import requests
from django.views.generic import DetailView
from django.http import HttpResponse

import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time
import sys
#import pickle
import json

from selenium.webdriver.firefox.options import Options

options = Options()
options.headless = True
 


def scrap(request):
    options = Options()
    #options.headless = True
    driver = webdriver.Firefox(options=options,executable_path = '/usr/local/bin/geckodriver')

    # driver = webdriver.Firefox(options=options,executable_path = '/usr/local/bin/geckodriver')
    #driver = webdriver.Firefox(executable_path = '/usr/local/bin/geckodriver')

    driver.get("https://manage.travel.rakuten.co.jp/portal/inn/mp_kanri_image_up.main")
    time.sleep(3)

    id1 = driver.find_element_by_name("f_id")
    id1.send_keys("first-t")

    pw = driver.find_element_by_name("f_pass")
    pw.send_keys("first-76")

    submit = driver.find_element_by_xpath("/html/body/table/tbody/tr/td/table[1]/tbody/tr/td/table/tbody/tr/td/table/tbody/tr[1]/td/table/tbody/tr[2]/td/form/table/tbody/tr[2]/td[3]/input")
    
    submit.click()
    #driver.quit()
    #return "nothing"

    time.sleep(5)

    driver.find_element_by_xpath("/html/body/table[2]/tbody/tr/td[3]/table[3]/tbody/tr[2]/td[1]/table/tbody/tr[3]/td/table/tbody/tr[1]/td[4]/input[1]").click()

    list_of_year_months = [
        {"year" : "2019年","month":"06月"},
        {"year" : "2019年","month":"07月"},
        {"year" : "2019年","month":"08月"},
        {"year" : "2019年","month":"09月"},
        {"year" : "2019年","month":"10月"},
        {"year" : "2019年","month":"11月"},
        {"year" : "2019年","month":"12月"},
        {"year" : "2020年","month":"01月"},
        {"year" : "2020年","month":"02月"},
        {"year" : "2020年","month":"03月"}
    ]
         
    my_list = [] 
    #for month in list_of_months: 
    for year_month in list_of_year_months: 
        year = year_month["year"]
        driver.find_element_by_link_text(year).click()
        
        month = year_month["month"]
        driver.find_element_by_link_text(month).click()

        time.sleep(3)

        
        jp_date = driver.find_element_by_xpath("/html/body/table[11]/tbody/tr/td/table/tbody/tr[1]/td[2]").text
        jp_date = jp_date.replace('年', '') #Special symbol means Year
        jp_date = jp_date.replace('月', '') #Special symbol means Month
        yearmonth = str(jp_date)
        table = driver.find_element_by_xpath("/html/body/table[11]/tbody/tr/td/table")

        #my_list = []

        rows = table.find_elements_by_tag_name("tr") # get all of the rows in the table

        my_dict = dict()
        base = 1
        rowcount = 1
        #day = 0
        for row in rows:

            print("####################  ROW " + str(rowcount) + " #################")

            # Get the columns (all the column 2)
            cols = row.find_elements_by_tag_name("td")#note: index start from 0, 1 is col 2
            first_col = cols[0].text 
            first_col_str = str(first_col)
            fca = first_col_str.split(':')
            first_col_first = fca[0]
            if 1 < len(fca):
                first_col_second = fca[1]

            tr_tuple_new = (1,2,3,13,14,24,25,35,36,46,47,57,68,69)
            tr_tuple_date_new = (4,15,26,37,48)
            
            colcount = 1 
            #print("First Col Str: " + first_col_str)
            #if rowcount not in tr_tuple_new and first != '':
            if rowcount not in tr_tuple_new:
                
                if rowcount in tr_tuple_date_new:
                    print("Hello")
                    for col in cols:
                        if col != cols[0] and col.text != '' and col.text != ' ':
                            base = col.text
                            break


                if rowcount not in tr_tuple_date_new:
                    #base = base[:-1]
                    base = str(base)
                    print("Base: " + base)       
                    base = base.replace('日', '') # Special symbol means "day" 
                    base = int(base)
                    print("Base"+ str(base) + "BASE")
                    #print(base)

                    day = 0 
                    for col in cols:
                        
                        if col != cols[0] and col.text != '' and col.text != ' ' and col.text != '済': # This special symbol means 'already'

                            print("######  COLUMN " + str(colcount) + " ######") 
                            
                            print("Room Type ID")
                            print(first_col_first)

                            print("Room Type Name")
                            print(first_col_second)

                            #print("StockFull")
                            #print(col.text)

                            coltextarray = col.text.split('/')
                            col_text_first = coltextarray[0]
                            col_text_second = coltextarray[0] 

                            print("Stock")
                            print(col_text_first)
                            print("Reservations")
                            print(col_text_second)
                            
                            
                            print("Date")
                            date = base + day

                            if date < 10:
                                date = "0"+str(date)
                            else:
                                date = str(date)
                            #print("day: " + days)

                            fulldate = yearmonth + date
                            print(fulldate)

                            my_dict = {
                                "date": fulldate,
                                "hotel_id": 4304,
                                "room_type_id": first_col_first,
                                "room_type_name": first_col_second,
                                "room_stock": col_text_first,
                                "reservations": col_text_second
                            }

                            my_list.append(my_dict)

                            day += 1
                            colcount += 1

            rowcount += 1
    driver.quit()


    #print(my_list)
    my_json = json.dumps(my_list,ensure_ascii=False)
    return HttpResponse(my_json)


	