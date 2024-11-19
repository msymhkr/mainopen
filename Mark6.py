from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import numpy as np

options = webdriver.ChromeOptions()
options.add_argument('no-sandbox')
options.add_argument('disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)
driver.get("https://bet.hkjc.com/ch/marksix/results")
driver.implicitly_wait(8)

for rqm in range(10, 0, -1):
    # search date
    seperoid = driver.find_element(By.XPATH, '//*[@class="date-input cp"]')
    seperoid.click()

    # set current month and year for search
    current_y = driver.find_element(By.XPATH, '//*[@class="dateRangePickerYear"]').text
    driver.implicitly_wait(3)
    current_m = driver.find_element(By.XPATH, '//*[@class="dateRangePickerMonth"]').text
    driver.implicitly_wait(3)
    # choose year
    rqy = 2024

    # choose month
    while not(current_m.__eq__(f"{rqm}" + "月") and current_y.__eq__(f"{rqy}")):
        driver.find_element(By.XPATH, '//*[@class="cursor-point prev-month arrow-icon arrow-icon-default-left false"]').click()
        current_y = driver.find_element(By.XPATH, '//*[@class="dateRangePickerYear"]').text
        driver.implicitly_wait(3)
        current_m = driver.find_element(By.XPATH, '//*[@class="dateRangePickerMonth"]').text
        driver.implicitly_wait(3)

    # choose start date
    sedate1 = "01"
    sedate1 = f"react-datepicker__day--0{sedate1}"
    searchdate1 = driver.find_element(By.XPATH, f'//*[contains(@class, "{sedate1}")]')
    driver.implicitly_wait(3)
    searchdate1.click()

    # choose end date
    for i in range(31, 28, -1):
        sedate2 = f"{i}"
        sedate2 = f"react-datepicker__day--0{sedate2}"
        try:
            searchdate2 = driver.find_element(By.XPATH, f'//div[contains(@class, "{sedate2}") and not(contains(@class, "outside-month"))]')
            driver.implicitly_wait(3)
            searchdate2.click()
            break
        except:
            pass

    driver.find_element(By.XPATH, '//*[@class="search-btn cta_m6"]').click()
    driver.implicitly_wait(2)
    time.sleep(2)
    cho_pd = driver.find_element(By.XPATH, '//*[@class="date-input cp"]')
    print("*****Chosen Date Period: " + str(cho_pd.get_attribute("value")))

    # print volume
    res_v = driver.find_elements(By.XPATH, '//*[@class="table-cell cell-id"]')
    driver.implicitly_wait(2)
    res_v = np.array(res_v)
    links1 = []
    for i in res_v:
        i = i.text
        links1.append(i)
    print("*****Volume no.: ")
    print(links1)

    # print date
    res_d = driver.find_elements(By.XPATH, '//*[@class="table-cell cell-date"]')
    driver.implicitly_wait(2)
    links2 = []
    for i in res_d:
        i = i.text
        links2.append(i)
    print("*****Volume Date: ")
    print(links2)

    # print ball text number
    res = driver.find_elements(By.XPATH, '//div[@class="img-box"]//img')
    driver.implicitly_wait(2)
    links = []
    for i in res:
        i = i.get_attribute('alt')
        links.append(int(i))
    links = np.array(links).reshape(-1, 7)
    print("*****Ball Results no.: ")
    print(links)

    # column stack
    wholelist = np.column_stack((links1, links2, links))
    wholelist = wholelist[~(wholelist == '').any(1),:]
    print("*****Whole list: ")
    print(wholelist)
    time.sleep(2)

    # Use numpy.savetxt() method to save the list as a CSV file
    with open("C:/Users/Chiu/Desktop/Final Mark Six Result List.csv", "a") as f:
        np.savetxt(f, wholelist, delimiter=", ", fmt='%s', header="", comments="")

# driver.quit()

