import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class maks_browser:
    def __init__(self):
        self.driver = webdriver.Firefox()
        self.driver.maximize_window()

    def loadBrowser(self, url):
        # Open Firefox Browser
        self.driver.get(url)

    def getDriver(self):
        return self.driver
    def closePopUp(self, className):
        try:
            self.driver.find_element_by_class_name(className).click()
        except:
            try:
                element = WebDriverWait(self.driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, className))
                )
                self.driver.execute_script("arguments[0].click();", element)
            except Exception as error:
                print('closePopup', error)
    def oneClick(self, xpath):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            element.click()
        except Exception as error:
            print('closePopup', error)
        # self.driver.find_element_by_xpath(xpath).click()
    def dropDown(self,check_value, ele, subele):
        try:
            self.driver.find_element_by_xpath(ele).click()
            time.sleep(2)
            found = False
            for _id, _li in enumerate(self.driver.find_element_by_xpath(subele).find_elements_by_tag_name('div')):
                if check_value.lower() in _li.text.lower():
                    _li.click()
                    found = True
            if found:
                return 0
            else:
                self.driver.find_element_by_xpath('//*[@id="contentplaceholder_0_column2placeholder_0_TimePlaceColumnLayout_LocationTime_Sitecorelabel2"]').click()
                return check_value
        except Exception as e:
            print(e)
            return check_value

    def sendKeys(self,id, inputvalue):
        self.driver.find_element_by_id(id).clear()
        self.driver.find_element_by_id(id).send_keys(inputvalue)
        pass

    def condition_click(self, condition_value, check_value, path):
        """
            condition_click:
                Funtion is used like toggle button
        """
        if condition_value == check_value:
            element = self.driver.find_element_by_xpath(path)
            self.driver.execute_script("arguments[0].click();", element)

    def closeBrowser(self):
        self.driver.close()



