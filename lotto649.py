import requests
import time
import pandas as pd
from selenium import webdriver
from lxml import html

url = 'http://www.taiwanlottery.com.tw/Lotto/Lotto649/history.aspx'

req = requests.get(url)
req.encoding = 'utf-8'

web_html = html.fromstring(req.content)

year_list = [y.text for y in web_html.xpath('//*[@id="Lotto649Control_history_dropYear"]/option')]
month_list = [m.text for m in web_html.xpath('//*[@id="Lotto649Control_history_dropMonth"]/option')]


driver = webdriver.Chrome()

driver.get(url)

driver.find_element_by_id('Lotto649Control_history_radYM').click()

time.sleep(1)

output_list = {'日期':[], '第一號碼':[], '第二號碼':[], '第三號碼':[], '第四號碼':[], '第五號碼':[], '第六號碼':[], '特別碼':[],}

for y in range(1,len(year_list)+1):
    
    driver.find_element_by_xpath('//*[@id="Lotto649Control_history_dropYear"]/option['+str(y)+']').click()

    for m in range(1,len(month_list)+1):
        
        driver.find_element_by_xpath('//*[@id="Lotto649Control_history_dropMonth"]/option['+str(m)+']').click()

        driver.find_element_by_id('Lotto649Control_history_btnSubmit').click()

        web_html = html.fromstring(driver.page_source)

        section_i = 0
        while True:
            section = web_html.xpath('//*[@id="Lotto649Control_history_dlQuery_SNo1_'+str(section_i)+'"]')
            if len(section) == 0:
                break

            this_date = web_html.xpath('//*[@id="Lotto649Control_history_dlQuery_L649_DDate_'+str(section_i)+'"]')[0].text
            print('%s'%(section_i))
            output_list['日期'].append(this_date)
            
            for i in range(1,7):
                this_number = web_html.xpath('//*[@id="Lotto649Control_history_dlQuery_SNo'+str(i)+'_'+str(section_i)+'"]')[0].text
                print(this_number, end='  ')
                
                index = list(output_list.keys())[i]
                output_list[index].append(this_number)
                
            last_number = web_html.xpath('//*[@id="Lotto649Control_history_dlQuery_No7_'+str(section_i)+'"]')[0].text
            print(last_number)
            output_list['特別碼'].append(last_number)

            section_i += 1
            print('---')

output = pd.DataFrame([], columns=list(output_list.keys()))
for k in output_list.keys():
    output[k] = output_list[k]

output.to_csv('result.csv')

driver.quit()



              
