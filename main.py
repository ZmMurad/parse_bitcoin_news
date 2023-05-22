import bs4
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager


def scrap(url):
    try:
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        driver.get(url)
        return driver.page_source
    except:
        print("Возникла ошибка при парсинге")
        return 
    


def get_news(class_for_search, page_source):
    soup=bs4.BeautifulSoup(page_source, "lxml")
    items=soup.findAll("div", class_=class_for_search)
    if len(items):
        return items
    print("Данные не найдены")
    

def get_news_name_date_link(items,class_for_search,url):
    list_out=[]
    for item in items[1:]:  
        link=url+item.find("a").get("href")
        name=item.find("a").find("img").get("alt")
        date=item.find("h6",class_=class_for_search).text
        list_out.append([link,name,date])
    if len(list_out):
        return list_out
    print("Данные не найдены")

def save_to_csv(filename, list_out):
    with open(filename,"w", encoding="utf8") as file:
        for item in list_out:
            file.write(f"{item[1]},{item[0]},{item[2]}\n")


if __name__=="__main__":
    page_source=scrap("https://www.coindesk.com/search?s=bitcoin")
    items=get_news("searchstyles__SearchCardWrapper-ci5zlg-21 hZygnS",page_source)
    list_out=get_news_name_date_link(items,"typography__StyledTypography-owin6q-0 lfNAOh","https://www.coindesk.com/")
    save_to_csv("data.csv",list_out)