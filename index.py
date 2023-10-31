
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import StaleElementReferenceException
from PIL import Image, ImageDraw
import re

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# proxy
# define custom options for the Selenium driver
options = Options()
# free proxy server URL
# proxy_server_url = "157.245.97.60"
# options.add_argument(f'--proxy-server={proxy_server_url}')

# Define search parameters
homeUrl = 'https://www.magasindepeinture.ch/en/ncs-color-chart-online.html'

# Initialize an instance of the chrome driver (browser)
options.page_load_strategy = 'eager'
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 10)

# Visit your target site
print("Go to ncs color chart")
print("Loading...")
driver.get(homeUrl)

# Type action
actions = ActionChains(driver)

try:  
    tableAllData = driver.find_elements(
    By.XPATH, "//tbody/tr")
    print(tableAllData)
    for rowIndex,rowData in enumerate(tableAllData):
        try:
            columnAllData = rowData.find_elements(
    By.XPATH, "./td")
            for columnIndex,columnData in enumerate(columnAllData):
                print(rowIndex,columnIndex)
                nameImg=columnData.text
                nameImg=re.sub(r'[^a-zA-Z0-9-]', '', nameImg)
                try:
                    colorCode= columnData.find_element(
    By.XPATH, "./div/div")
                    background_color = colorCode.value_of_css_property('background-color')
                    # print(background_color)
                    width, height = 237, 79
                    image = Image.new("RGB", (width, height), "white")
                    draw = ImageDraw.Draw(image)                    
                    draw.rectangle(((5, 5), (232, 74)), fill=background_color)

                    # Save the image to a file
                    image.save(nameImg+".jpg")
                except NoSuchElementException:
                    print("Not found color data")
                

        except NoSuchElementException:
             print("Not found column data")

except NoSuchElementException:
    print("Not found table all data")

print("Close browser")
driver.quit()
