import time
import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

# Setup Chrome
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://quotes.toscrape.com/scroll")

time.sleep(2)  # initial wait

# Infinite scroll
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)  # wait for new content
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Find all quote containers
quote_blocks = driver.find_elements(By.CLASS_NAME, "quote")

# Prepare CSV
with open("quotes_day4.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Quote", "Author", "Tags"])
    
    for block in quote_blocks:
        try:
            quote = block.find_element(By.XPATH, ".//span[@class='text']").text
        except:
            quote = ""
        try:
            author = block.find_element(By.XPATH, ".//small[@class='author']").text
        except:
            author = ""
        try:
            tags = block.find_element(By.XPATH, ".//div[@class='tags']").text
        except:
            tags = ""
        
        writer.writerow([quote, author, tags])

print("Scraping completed! CSV saved as quotes_day4.csv")
driver.quit()
