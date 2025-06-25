import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

def scrape_data():
    options = Options()
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    )

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 5)

    players_pitchers_data = []
    teams_data = []
    section_headers = {"East", "Central", "West", "A.L.", "N.L."}

    try:
        driver.get("https://www.baseball-almanac.com/yearmenu.shtml")
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "table a")))
    
        tables = driver.find_elements(By.TAG_NAME, 'table')
        al_links = tables[0].find_elements(By.TAG_NAME, "a")
        nl_links = tables[1].find_elements(By.TAG_NAME, 'a')
        print("Found", len(al_links), "american league links.")
        print("Found", len(nl_links), "national league links.")
        all_links = al_links + nl_links
    
        all_hrefs = []
        for link in all_links:
            year = link.text.strip()
            href = link.get_attribute('href')
        
            if "a.shtml" in href:
                league = 'AL'
            elif "n.shtml" in href:
                league = 'NL'
            else:
                continue
            all_hrefs.append((year,href,league))

        all_years = sorted(set(year for year, _, _ in all_hrefs if year.isdigit()), reverse=True)

        seen = set()
        filtered_links = []
        for (year, url, league) in all_hrefs:
            if year.isdigit() and int(year) >= 2000:
               key = (year, league)
               if key not in seen:
                    seen.add(key)
                    filtered_links.append((year, url, league))
    
        filtered_links.sort(key=lambda x: (x[0], x[2])) 
      
        for year, url, league in filtered_links:
            print(f"Year: {year}, League: {league}, URL: {url}")
            driver.get(url)
            wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "table")))
            tables = driver.find_elements(By.TAG_NAME, 'table')
        
            for i in range(2):
                rows = tables[i].find_elements(By.TAG_NAME, 'tr')
                table_header = ""
                try:
                    h2 = rows[0].find_element(By.TAG_NAME, "h2")
                    table_header = h2.text.strip()
                except NoSuchElementException:
                    table_header = 'Unknown Selection'
                for row in rows[1:]:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if len(cells) != 5:
                       continue
                    row_data = {
                        "Section": table_header,
                        "Statistic": cells[0].text.strip(),
                        "Name": cells[1].text.strip(),
                        "Team": cells[2].text.strip(),
                        "#": cells[3].text.strip(),
                        "Top 25": cells[4].text.strip(),
                        "Year": year,
                        "League": league
                    }
                    players_pitchers_data.append(row_data)
            if len(tables) >= 3:
                rows = tables[2].find_elements(By.TAG_NAME, "tr")
                headers = ['Team', 'W', 'L', 'T', 'WP', 'GB', 'Year', 'League']

                for row in rows[1:]:
                    cells = row.find_elements(By.TAG_NAME, 'td')
                    if not cells:
                       continue
                    if cells[0].text.strip() in section_headers:
                       continue
                    if "Team | Roster" in cells[0].text:
                       continue

                    row_dict = {}
                    for i, header in enumerate(headers[:-2]):
                        row_dict[header] = cells[i].text.strip() if i < len(cells) else ''
                    row_dict['Year'] = year
                    row_dict['League'] = league
                    teams_data.append(row_dict)

    except Exception as e:
        print("Couldn't load the web page")
        print(f"Exception: {type(e).__name__} {e}")

    finally:
        driver.quit()

    df_pp = pd.DataFrame(players_pitchers_data)
    df_teams = pd.DataFrame(teams_data)
    
    return df_pp, df_teams

def main():
    df_pp, df_teams = scrape_data()
    df_pp.to_csv("csv/players_pitchers_data.csv", index=False)
    df_teams.to_csv("csv/teams_data.csv", index=False)
    
if __name__ == "__main__":
    main()
