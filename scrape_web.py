# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 06:41:12 2019

@author: Rainer
"""

from selenium import webdriver
from selenium.webdriver.support.ui import Select #helps select dropdown menus


# save url

url = "https://raie.tallinn.ee/open_raie.php"

# download options - allows selenium chrome to download files immediately on click

download_dir = ""
options = webdriver.ChromeOptions()

profile = {"plugins.plugins_list": [{"enabled": False, "name": "Chrome PDF Viewer"}], # Disable Chrome's PDF Viewer
               "download.default_directory": download_dir , "download.extensions_to_open": "applications/pdf"}
options.add_experimental_option("prefs", profile)


# new chrome session

driver = webdriver.Chrome(chrome_options=options)
driver.implicitly_wait(30)
driver.get(url)


# select 'raieluba' date fields and 'otsi'

raieluba = driver.find_element_by_xpath("/html/body/div[2]/div/form/table/tbody/tr[1]/td[2]/input[1]")
otsi = driver.find_element_by_xpath("/html/body/div[2]/div/form/table/tbody/tr[6]/td[1]/input")
fday = Select(driver.find_element_by_xpath("/html/body/div[2]/div/form/table/tbody/tr[5]/td[2]/select[1]"))
fmonth = Select(driver.find_element_by_xpath("/html/body/div[2]/div/form/table/tbody/tr[5]/td[2]/select[2]"))
fyear = Select(driver.find_element_by_xpath("/html/body/div[2]/div/form/table/tbody/tr[5]/td[2]/select[3]"))
tday = Select(driver.find_element_by_xpath("/html/body/div[2]/div/form/table/tbody/tr[5]/td[2]/select[4]"))
tmonth = Select(driver.find_element_by_xpath("/html/body/div[2]/div/form/table/tbody/tr[5]/td[2]/select[5]"))
tyear = Select(driver.find_element_by_xpath("/html/body/div[2]/div/form/table/tbody/tr[5]/td[2]/select[6]"))

fday.select_by_visible_text('1')
fmonth.select_by_visible_text('jaanuar')
fyear.select_by_visible_text('2018')
tday.select_by_visible_text('31')
tmonth.select_by_visible_text('detsember')
tyear.select_by_visible_text('2018')

#click filters

raieluba.click()
otsi.click()

# create loop to dowload all pdfs on all pages

rownr = 2
pagenr = 2

while pagenr < 99:
    while rownr < 22:
        driver.get(driver.find_element_by_xpath("/html/body/div[2]/div/table/tbody/tr[" +str(rownr)+ "]/td[6]").find_element_by_css_selector('a').get_attribute('href'))
        rownr += 1
    nextpage = driver.find_element_by_partial_link_text('>>')
    nextpage.click()
    pagenr += 1
    rownr = 2
    



