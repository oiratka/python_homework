import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException


driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get("https://owasp.org/www-project-top-ten/")
try:
    top_10_h2 = driver.find_element(By.CSS_SELECTOR, '#top-10-web-application-security-risks')
    parent_section = top_10_h2.find_element(By.XPATH, './ancestor::section')
    link_elements = parent_section.find_elements(By.TAG_NAME, 'a')
    links=[]
    for link in link_elements:
        name = link.text.strip()
        url = link.get_attribute('href')
        if name and url:
            print(f"{name}: {url}")
            links.append({"name": name, "url": url})
    df = pd.DataFrame(links)
    df.to_csv("owasp_top_10.csv", index=False)
except NoSuchElementException as e:
        print("Unable to locate the Top 10 container")
        print(f"Exception: {type(e)._name_} {e}")
finally:
    driver.quit()

    


