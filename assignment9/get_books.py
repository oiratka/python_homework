import pandas as pd
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
try:
    driver.get("https://durhamcounty.bibliocommons.com/v2/search?query=learning%20spanish&searchType=smart")
    
    li_elements = driver.find_elements(By.CSS_SELECTOR, "li.cp-search-result-item")
    results = []
    for li in li_elements:
        try:
            title_element = li.find_element(By.CSS_SELECTOR, ".cp-title .title-content")
            title = title_element.text
            print(f"Title: {title}")
            author_elements = li.find_elements(By.CSS_SELECTOR, ".cp-author-link .author-link")
            authors = [a.text for a in author_elements]
            author_text = "; ".join(authors)
            print(f"Author(s): {author_text}")
            div_element = li.find_element(By.CSS_SELECTOR, "div.cp-format-info")
            span_element = div_element.find_element(By.CSS_SELECTOR, ".display-info-primary")
            format_year = span_element.text
            print(f"Format-Year: {format_year}")
            dict_text = {
                'Title': title, 
                'Author': author_text, 
                "Format-Year": format_year
                }
            results.append(dict_text)
            
        except Exception as e:
            print("Couldn't extract title from one of the items")
            continue
    df = pd.DataFrame(results)
    df.to_csv("get_books.csv", index=False)

    with open("get_books.json", "w") as json_file:
        json.dump(results, json_file, indent=4)
except Exception as e:
    print("couldn't load the web page")
    print(f"Exception: {type(e)._name_} {e}")
finally:
    driver.quit()




