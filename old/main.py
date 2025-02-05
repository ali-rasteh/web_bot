from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import tempfile

# Setup Selenium WebDriver
temp_dir = tempfile.mkdtemp()  # Create a unique temp directory
options = webdriver.ChromeOptions()
# options.add_argument("--headless")  # Run in background
options.add_argument(f"--user-data-dir={temp_dir}")
options.add_argument("--no-sandbox")  # Useful for running in some environments
driver = webdriver.Chrome(options=options)

# Open the embassy appointment page
driver.get("https://testpages.herokuapp.com/styled/basic-html-form-test.html")
print("Page title: ", driver.title)

# Fill in form fields
driver.find_element(By.NAME, "username").send_keys("TestUser")
driver.find_element(By.NAME, "password").send_keys("TestPassword")
driver.find_element(By.NAME, "comments").send_keys("This is a test comment.")


# Click submit
submit_button = driver.find_element(By.XPATH, "//input[@type='submit']")
submit_button.click()

# Wait for confirmation
time.sleep(2)

# Take screenshot (optional for debugging)
driver.save_screenshot("confirmation.png")

input("Press Enter to continue...")

# Close browser
driver.quit()
