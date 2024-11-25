from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Initialize the WebDriver
driver = webdriver.Chrome()

# Open the first webpage
url = "https://cbl.gov.ly/monetary-and-banking/"
driver.get(url)

# Wait for the first button (تحميل) to be clickable
WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.LINK_TEXT, "تحميل"))
)

# Click the first button
first_button = driver.find_element(By.LINK_TEXT, "تحميل")
first_button.click()

# Switch to the second page (if it opens in a new tab)
time.sleep(2)  # Wait briefly for the page to load
driver.switch_to.window(driver.window_handles[-1])  # Switch to the latest tab

# Wait for the specific button on the second page
second_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, '//*[@id="icon"]/cr-icon'))
)

# Click the specific button
ActionChains(driver).move_to_element(second_button).click(second_button).perform()

# Close the browser
driver.quit()
