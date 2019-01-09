from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
from bs4 import BeautifulSoup as bs
import time
import logging
from setlog import setlog
logging = setlog()


class TradeSpider(object):

    def __init__(self):
        logging.info("start TradeSpider!")

    def setDriver(self):
        # self.driver = webdriver.PhantomJS()
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Firefox(
            firefox_options=options, executable_path='./geckodriver')

    # ---login----
    def login(self, ac, pw):
        url = "https://www.trademap.org/Country_SelProduct_TS.aspx"
        self.driver.get(url)
        wait = WebDriverWait(self.driver, 10)
        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="ctl00_MenuControl_Label_Login"]'))).click()
        # Switch  iframe
        wait.until(
            EC.frame_to_be_available_and_switch_to_it('iframe_login'))
        # UserName
        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, '//*[@id="PageContent_Login1_UserName"]'))).send_keys(ac)
        # Password
        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH,
                 '//*[@id="PageContent_Login1_Password"]'))).send_keys(pw)
        # Click
        self.driver.find_element_by_xpath(
            '//*[@id="PageContent_Login1_Button"]').click()

        # Check
        self.driver.switch_to_default_content()
        soup = bs(self.driver.page_source, "lxml")
        if "Trade Map" in soup.title.text:
            logging.info("ITC login sucess!")
        else:
            logging.error("login faild")


    # Records
    def setRecords(self, n):
        '''
        Records = ["Exports", "Imports"]
        option = [1,2]
        '''
        wait = WebDriverWait(self.driver, 10)
        wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                '/html/body/form/div[3]/div[5]/table/tbody/tr[4]/td[2]/div/table/tbody/tr/td[3]/div[1]/select/option[{}]'.format(
                    str(n))
            ))).click()
        Records = ["Exports", "Imports"]
        logging.debug("setRecords " + Records[n - 1])

    # Indicators
    def setIndicators(self, n):

        '''
        Indicators = ["Values", "Quantities"]
        option = [1,2]
        '''
        xpath = '/html/body/form/div[3]/div[5]/table/tbody/tr[4]/td[2]/div/table/tbody/tr/td[3]/div[4]/select/option[{}]'.format(
            str(n))
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()
        Indicators = ["Values", "Quantities"]
        logging.debug("setIndicators " + Indicators[n-1])
    # Timeseries
    def setTimePage(self):

        wait = WebDriverWait(self.driver, 10)
        wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                '/html/body/form/div[3]/div[5]/table/tbody/tr[4]/td[2]/div/table/tbody/tr/td[3]/div[2]/select/option[4]'
            ))).click()

        # Time Period = "20 per page"
        wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                '/html/body/form/div[3]/table/tbody/tr[2]/td/div[1]/table/tbody/tr[2]/td[6]/div/select/option[7]'
            ))).click()

        # Rows per page = "300 per page"
        wait.until(
            EC.element_to_be_clickable((
                By.XPATH,
                '/html/body/form/div[3]/table/tbody/tr[2]/td/div[1]/table/tbody/tr[2]/td[7]/div/select/option[5]'
            ))).click()
        logging.debug("set TimePage")

    # Products
    def selectProducts(self, n):
        '''
        n: 選取 Products的第n個options
        '''
        n = str(n)
        time.sleep(3)
        wait = WebDriverWait(self.driver, 10)
        xpath = "/html/body/form/div[3]/div[5]/table/tbody/tr[1]/td/div/table/tbody/tr/td[3]/select/option[{}]".format(
            n)
        item = wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).text
        logging.info("selectProducts: " + item)
        wait.until(EC.element_to_be_clickable((By.XPATH, xpath))).click()

    def save(self, filename):
        table_source = self.driver.find_element_by_xpath(
            '/html/body/form/div[3]/table/tbody/tr[3]/td').get_attribute('innerHTML')
        df = pd.read_html(table_source)[0]
        # print(df.head)

        df.to_pickle(filename+'.pickle')
        logging.info("save {}.pickle".format(filename))

    def showdf(self):
        table_source = self.driver.find_element_by_xpath(
            '/html/body/form/div[3]/table/tbody/tr[3]/td').get_attribute(
                'innerHTML')
        df = pd.read_html(table_source)[0]
        print(df.head)

    def close(self):
        self.driver.close()
        logging.info("Close Driver!!")


if __name__ == "__main__":
    ac = "ponggung1986@gmail.com"
    pw = "********"
    s = TradeSpider()
    s.setDriver()
    s.login(ac, pw)
    s.setTimePage()
    for n in [5, 12, 10]:
        s.selectProducts(n)
    s.setRecords(1)
    s.setIndicators(1)
    # s.save("test")
    s.showdf()
    s.close()
