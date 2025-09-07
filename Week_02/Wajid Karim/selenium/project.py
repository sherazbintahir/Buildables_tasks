from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome()
query = "headphones"
file = 0
for i in range(1, 15):
    driver.get(f"https://www.amazon.com/s?k={query}&page={i}crid=2MNRYI87W2U3W&sprefix=headpho%2Caps%2C448&ref=nb_sb_ss_p13n-pd-dpltr-ranker_ci_hl-bn-left_1_7")

    elem = driver.find_elements(By.CLASS_NAME, "puis-card-container")

    print(f"{len(elem)} elements found")
    for elem in elem:
        d = elem.get_attribute("outerHTML")
        with open(f"selenium/data/{query}_{file}.html", "w", encoding="utf-8") as f:
            f.write(d)
            file += 1
              
    #print(elem.get_attribute("outerHTML"))
    #print(elem.text)
    time.sleep(5)
driver.quit()


