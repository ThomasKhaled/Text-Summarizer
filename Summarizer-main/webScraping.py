from selenium import webdriver


class webScraping:
    def ReadFromWebSite(self, URL='https://markmanson.net/best-articles'):
        PATH = 'chromedriver.exe'
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        driver = webdriver.Chrome(PATH,options=option)
        driver.get(URL)
        bodyElement = driver.find_element_by_tag_name('body')
        return str(bodyElement.text)