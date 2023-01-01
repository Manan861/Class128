from selenium import webdriver
from bs4 import BeautifulSoup
import time
import csv
import requests
START_URL = "https://exoplanets.nasa.gov/exoplanet-catalog/"
browser = webdriver.Chrome("chromedriver.exe")
browser.get(START_URL)
time.sleep(10)
def scrape():
    headers = ["name", "light_years_from_earth", "planet_mass", "stellar_magnitude", "discovery_date","hyperlink","planet_type","planet_radius","orbital_radius","orbital_period","eccentricity"]
    planet_data = []
    for i in range(0, 428):
        soup = BeautifulSoup(browser.page_source, "html.parser")
        current_page_no=int(soup.find_all("input",attrs={"class","page_num"})[0].get("value"))
        if current_page_no<i:
            browser.find_element(By.XPATH.value='[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
        elif current_page_no>i:
            browser.find_element(By.XPATH.value='[@id="primary_column"]/footer/div/div/div/nav/span[1]/a').click()
        else:
            break
        for ul_tag in soup.find_all("ul", attrs={"class", "exoplanet"}):
            li_tags = ul_tag.find_all("li")
            temp_list = []
            for index, li_tag in enumerate(li_tags):
                if index == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")
            hyperlink_li_tag=li_tags[0]
            temp_list.append("https://expoplanets.nasa.gov"+hyperlink_li_tag.find_all("a",href=True)[0]["href"])
            planet_data.append(temp_list)
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()
    with open("scrapper_2.csv", "w") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(headers)
        csvwriter.writerows(planet_data)

new_planets_data=[]
def scrape_more_data(hyperlink):
    try:
        page=requests.get(hyperlink)
        soup=BeautifulSoup(page.content,"html.parser")
        temp_list=[]
        for tr_tag in soup.find_all("tr",attrs={"class":"fact_row"}):
            td_tags=tr_tag.find_all("td")
            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all("div",attrs={"class":"value"})[0].contents[0])
                except:
                    temp_list.append("")
        new_planets_data.append(temp_list)
    except:
        time.sleep(1)
        scrape_more_data(hyperlink)
for index,data in enumerate(planet_data):
    scrape_more_data(data[5])
    print("scraping is completed")
print(new_planets_data[0,10])
scrape()
for data in planet_data: 
    scrape_more_data(data[5])


