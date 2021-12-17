from os import link
import bs4
import selenium
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd



def web_driver():

    options = Options
    options = webdriver.ChromeOptions()
    options.add_argument("no-sandbox")
    options.add_argument('--dns-prefetch-disable')
    options.add_experimental_option('useAutomationExtension', False)
    # options.add_argument("--headless")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    prefs = {"profile.managed_default_content_settings.images": 2}
    options.add_experimental_option("prefs", prefs)
    options.add_argument("--disable-extensions")
    return webdriver.Chrome(executable_path='D:/chromedriver_96/chromedriver.exe')



def click_Operation():
    global driver
    global name
    global city
    driver = web_driver()
    url = 'https://wayspa.com/'
    driver.get(url)
    time.sleep(5)

    name = input('-------------->>> Enter Spa or Service Name: ---------->>>: ')
    city = input('-------------->>> Enter Cite Name: -------------------->>>: ')
    

    time.sleep(3)
    try:
        
        cut = driver.find_element(By.CLASS_NAME,'mc-closeModal')
        if cut:
            cut.click()
        else:
            pass    
    except:
        pass

    driver.maximize_window()
    driver.implicitly_wait(20)

    service_input = driver.find_element(By.XPATH,'/html/body/main/div/div/section/div[3]/div/div/div/div/div/section/div/form/div[1]/input')
    service_input.click()
    service_input.send_keys(name)
    time.sleep(3)
    
    location = driver.find_element(By.XPATH,'/html/body/main/div/div/section/div[3]/div/div/div/div/div/section/div/form/div[2]/input')
    location.click()
    location.send_keys(city)
    time.sleep(2)

    search = driver.find_element(By.XPATH,'/html/body/main/div/div/section/div[3]/div/div/div/div/div/section/div/form/input[5]')
    search.click()
    time.sleep(12)
   
def link_collect():
    all_links =[]

    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        load = driver.find_element(By.XPATH,'//*[@id="mtt-wrapper"]/div/section/div/section[2]/div[2]/button')
        while load:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            load.click()
            time.sleep(3)       
    except:
        pass

    links = driver.find_elements(By.XPATH,'//*[@id="search-container"]/article/div/a')
    for link in links:
        lnk = (link.get_attribute('href'))
        print(lnk)


        lnk ={
            'Links':lnk
        }

        all_links.append(lnk)

        df = pd.DataFrame(all_links)
        df.to_csv('links.csv')
    print('All Links Collected')
    print('Please Wait For The Data Scraping Process')
    driver.close()


def data_scraper():
    driver = web_driver()
    df = pd.read_csv('links.csv')
    ln = df['Links'].values
    links = []
    main_data = []
    for i in ln:
        driver.get(i)
        time.sleep(5)   

        try:
            cut = driver.find_element(By.CLASS_NAME,'mc-closeModal')
            time.sleep(1)
            cut.click()
        except:
            pass    

        try:
            shop_name = driver.find_element(By.XPATH,'//*[@id="overview"]/div[2]/div[1]/h1').text
            print(shop_name)
        except:
            shop_name = ''
        try:    
            adress = driver.find_element(By.XPATH,'//*[@id="overview"]/div[2]/div[1]/div/small').text
            # print(adress)
        except:
            adress = ''
        try:
            website = driver.find_element(By.XPATH,'//*[@id="overview"]/div[4]/div[2]/div[1]/div[1]/a').get_attribute('href')
            # print(website)
        except:
            website = ''
        try:
            phone = driver.find_element(By.XPATH,'//*[@id="overview"]/div[4]/div[2]/div[1]/div[2]/a').get_attribute('href').replace('tel:','').replace(',','')
            # print(phone)
        except:
            phone = ''

        try:
            des = driver.find_element(By.XPATH,'//*[@id="mtt-wrapper"]/div/section/section[2]/div/div[2]/div[1]/div[1]/div[1]').text
        except:
            des = ''
        try:
            imgs=driver.find_elements(By.XPATH,'/html/body/main/div/div/section/section[2]/div/div[1]/div[3]/div[1]/div/div/div/div/div/a')

            all_img = set()
            for img in imgs:
                img_url = img.get_attribute('href')
                # all_img.append(img_url)
                all_img.add(img_url)
            list_img = []
            for al in all_img:
                al = al.replace(',',', \n')  
                list_img.append(al)  

                
        except:    
            img_url =''

        data_dict = {

            'Name':shop_name,
            'Adress':adress,
            'Website':website,
            'Phone':phone,
            'Description':des,
            'URL':i,
            'Image_Url':list_img
        }
        
        main_data.append(data_dict)
        df = pd.DataFrame(main_data)
        # df.to_csv(f"{name}_{city}.csv")
        df.to_csv('spa_in_Victoria2.csv')

  
    print('Scraping Completed')
    driver.close()

if __name__ == '__main__':

    # click_Operation()
    # link_collect()
    data_scraper()
    

    







