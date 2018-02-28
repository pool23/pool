from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time

driver = webdriver.Firefox()
driver.get("https://online.citi.com/US/JRS/pands/detail.do?ID=CurrentRates&JFP_TOKEN=8IVCO3CE")
assert "Citibank" in driver.title

time.sleep(10)
select = driver.find_element_by_xpath('//span[@class="ui-selectmenu-item-header"]')
select.click()

# select = Select(driver.find_element_by_id('RegionalPricingLocation-snapshot'))
# for element in select.options:
#     if element.get_attribute("value") == "AA":
#         #select.select_by_visible_text("AA")
#         select.select_by_index(1)
#     print(element.get_attribute("value"))










#select.select_by_value("AA")

#select = Select(driver.find_element_by_id('RegionalPricingLocation-snapshot'))

#options = [x for x in select.find_elements_by_tag_name("option")]
#select.select_by_visible_text('AA')
#select.select_by_value('1')
#driver.close()


