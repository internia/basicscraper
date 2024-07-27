from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from bs4 import BeautifulSoup

def get_browser(browser_name="chrome"):
    if browser_name.lower() == "chrome":
        options = ChromeOptions()
        options.add_argument("--headless")
        service = ChromeService(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    elif browser_name.lower() == "firefox":
        options = FirefoxOptions()
        options.add_argument("--headless")
        service = FirefoxService(GeckoDriverManager().install())
        driver = webdriver.Firefox(service=service, options=options)
    elif browser_name.lower() == "edge":
        options = EdgeOptions()
        options.add_argument("--headless")
        service = EdgeService(EdgeChromiumDriverManager().install())
        driver = webdriver.Edge(service=service, options=options)
    else:
        raise ValueError(f"Unsupported browser: {browser_name}")
    return driver

try:
    print("Enter search term: ")
    searchterm = input()
    URL = "https://www.vinted.co.uk/catalog?search_text={}".format(searchterm) #TODO: change the search term to be defined by a user input string from website
    driver = get_browser("firefox")  #TODO: change based on detected browser on web load
    driver.get(URL)
    print("Fetched the URL...")

    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "feed-grid__item")))

    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()  

    items_holder = soup.find_all("div", class_="feed-grid__item")
    print(f"Found {len(items_holder)} items...")

    for index, item in enumerate(items_holder):
        try:
            # extracting  overlay link element
            overlay_link = item.find("a", class_="new-item-box__overlay new-item-box__overlay--clickable")
            if overlay_link and 'title' in overlay_link.attrs:
                title_attribute = overlay_link['title']
                # splitting  title attribute to extract relevant details
                title_parts = title_attribute.split(', ')
                item_title_text = title_parts[0] if len(title_parts) > 0 else 'N/A'
                item_price_text = title_parts[1].replace('price: ', '') if len(title_parts) > 1 else 'N/A'
                item_brand_text = title_parts[2].replace('brand: ', '') if len(title_parts) > 2 else 'N/A'
                item_size_text = title_parts[3].replace('size: ', '') if len(title_parts) > 3 else 'N/A'
            else:
                item_title_text = 'N/A'
                item_price_text = 'N/A'
                item_brand_text = 'N/A'
                item_size_text = 'N/A'
                print(f"Item {index + 1}: Title attribute not found.")

            # extracting the image URL 
            image_div = item.find("div", class_="new-item-box__image")
            item_img_tag = image_div.find("img", class_="web_ui__Image__content") if image_div else None
            if not item_img_tag:
                print(f"Item {index + 1}: Image not found.")
                
            item_img_url = item_img_tag['src'] if item_img_tag else 'N/A'

            print(f"Item {index + 1}:")
            print(f"Title: {item_title_text}")
            print(f"Size: {item_size_text}")
            print(f"Brand: {item_brand_text}")
            print(f"Price: {item_price_text}")
            print(f"Image URL: {item_img_url}")
            print("-" * 40)
        except Exception as e:
            print(f"Error processing item {index + 1}: {e}")

except Exception as e:
    print(f"An error occurred: {e}")

