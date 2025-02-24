from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import tempfile
import ntplib
from datetime import datetime, timezone, timedelta
import pytz
import capsolver
import sys
import os
import base64
import random

# import pytesseract
# # pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
# from PIL import Image
# import io




manual_captcha = False

capsolver.api_key = "CAP-A7BAF779B2EC08D9513D7F5D279FEF58F9FE055EBF6D80E5691C2FA330500777"
url = "https://service2.diplo.de/rktermin/extern/appointment_showMonth.do?locationCode=tehe&realmId=22&categoryId=3069"  # Adjust path if necessary
# url = "file:///C:/Users/alira/OneDrive/Desktop/Current_works/web_bot/form_main.html"
# start_time = "2025-02-12 02:30:01 UTC"
start_time = "08:35:01"
# time_format = "%Y-%m-%d %H:%M:%S %z"
captcha_sleep_time = 5.0
general_wait_time = 10.0

last_name = "RASTEH"
first_name = "VAHID"
email = "vahid.rasteh75@gmail.com"
passport_number = "V69382678"
phone_number = "09372676565"
nationality = "Iran"
star_value = '1'
other_value = '-'
    




NTP_SERVERS = ["time.google.com", "pool.ntp.org", "time.nist.gov", "europe.pool.ntp.org"]
# NTP_SERVERS = ["time.nist.gov", "europe.pool.ntp.org"]

def get_ntp_time(ntp_server="time.google.com", timezone_str="Asia/Tehran", retries=5):
    """Fetches the exact time from an NTP server and converts it to Germany's timezone with retry logic."""
    for attempt in range(retries):
        try:
            client = ntplib.NTPClient()
            response = client.request(ntp_server, version=3)
            
            # Convert to UTC datetime
            # utc_time = datetime.utcfromtimestamp(response.tx_time).replace(tzinfo=timezone.utc)
            utc_time = datetime.fromtimestamp(response.tx_time, tz=timezone.utc)

            # Convert to Germany's timezone
            time_zone = pytz.timezone(timezone_str)
            local_time = utc_time.astimezone(time_zone)

            return local_time

        except Exception as e:
            print(f"Attempt {attempt + 1}: Failed to get time from {ntp_server} - {e}")

        time.sleep(1)  # Wait before retrying

    print("Failed to get time from all NTP servers after multiple attempts.")
    return None


def wait_until(start_time_str, sleep_interval=1):
    """Waits until the specified start time while printing the remaining time."""
    start_time = datetime.strptime(start_time_str, "%H:%M:%S").time()

    server_idx = 0
    while True:
        server_idx = (server_idx + 1) % len(NTP_SERVERS)
        ntp_server = NTP_SERVERS[server_idx]
        current_time = get_ntp_time(ntp_server)

        if not current_time:
            print("Using system time as fallback.")
            current_time = datetime.now(pytz.timezone("Europe/Berlin"))

        current_time_only = current_time.time()

        # Calculate remaining time
        current_datetime = current_time.replace(microsecond=0)
        start_datetime = current_datetime.replace(hour=start_time.hour, minute=start_time.minute, second=start_time.second)

        if start_datetime < current_datetime:
            # If the start time is for the next day
            start_datetime += timedelta(days=1)

        remaining_time = start_datetime - current_datetime
        
        if remaining_time.total_seconds() <= 0:
            break

        print(f"Time remaining: {remaining_time}", end="\r")
        time.sleep(sleep_interval)
    


class page_base():
    def __init__(self, driver):
        self.driver = driver
        self.page_loaded = False


    def page_loaded_check(self):
        # Wait for CAPTCHA input field to load
        WebDriverWait(self.driver, general_wait_time).until(
            EC.presence_of_element_located((By.ID, "appointment_captcha_month_captchaText"))
        )
        print("Page 1 loaded successfully!")





class page_1():
    def __init__(self, driver):
        self.driver = driver
        
        print("Page 1 instance loaded successfully!")


    def page_loaded_check(self):
        # Wait for CAPTCHA input field to load
        WebDriverWait(self.driver, general_wait_time).until(
            EC.presence_of_element_located((By.ID, "appointment_captcha_month_captchaText"))
        )
        print("Page 1 loaded successfully!")

    
    def init_elements(self):
        self.captcha_input = self.driver.find_element(By.ID, "appointment_captcha_month_captchaText")
        self.submit_button = self.driver.find_element(By.ID, "appointment_captcha_month_appointment_showMonth")
        self.captcha_element = self.driver.find_element(By.XPATH, "//div[contains(@style, 'background:white url')]")
        
        print("Page 1 elements initialized successfully!")


    def get_captcha(self):
        # Locate CAPTCHA Image (Base64)
        captcha_style = self.captcha_element.get_attribute("style")

        # Extract Base64 CAPTCHA data
        base64_start = "data:image/jpg;base64,"
        start_index = captcha_style.find(base64_start) + len(base64_start)
        end_index = captcha_style.find("')", start_index)
        self.captcha_base64 = captcha_style[start_index:end_index]
        print(f"Extracted CAPTCHA Base64: {self.captcha_base64}...")

        print("CAPTCHA image loaded successfully!")


    def solve_captcha(self):

        if manual_captcha:
            # captcha_image.show()
            self.captcha_text = input("Please enter the CAPTCHA text displayed: ").strip()
        else:
            # Add padding if necessary
            missing_padding = len(self.captcha_base64) % 4
            if missing_padding:
                self.captcha_base64 += '=' * (4 - missing_padding)

            captcha_bytes = base64.b64decode(self.captcha_base64)

            # captcha_image = Image.open(io.BytesIO(captcha_bytes))
            # captcha_image.save("test.png")
            # # Use OCR to extract text
            # captcha_text = pytesseract.image_to_string(captcha_image, config='--psm 6').strip()


            # img_path = './captcha.png'
            # with open(img_path, 'rb') as f:
            solver_out = capsolver.solve({
                "type": "ImageToTextTask",
                # "websiteURL": "https://www.example.com",
                # "module": "common",
                "module": "module_005",
                # "body": captcha_base64,
                # "body": base64.b64encode(f.read()).decode('utf-8'),
                "body": base64.b64encode(captcha_bytes).decode('utf-8')
            })
            self.captch_confidence = solver_out["confidence"]
            self.captcha_text = solver_out["text"]

        print(f"Solved CAPTCHA text: {solver_out}")


    def reload_captcha(self):
        self.load_picture_button = WebDriverWait(driver, general_wait_time).until(
            EC.element_to_be_clickable((By.ID, "appointment_captcha_month_refreshcaptcha"))
        )
        # Click the button
        self.load_picture_button.click()

        print("CAPTCHA image reloaded successfully!")


    def fill_captcha(self):
        # Fill in the CAPTCHA text
        self.captcha_input.send_keys(self.captcha_text)

        # Submit the form
        self.submit_button.click()
        print("CAPTCHA submitted successfully!")


    def check_handler(self):
        # Wait for new page to load by checking a known element on Page 2
        try:
            result = WebDriverWait(self.driver, general_wait_time).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@onclick, 'startCommitRequest') and .//img[contains(@src, 'images/go-next.gif')]]"))
            )
            print("Page 1 completed successfully!")
        except Exception as e:
            print(f"Failed to load Page 2: {e}")


    def handle_page(self):
        self.page_loaded_check()
        self.init_elements()
        self.get_captcha()
        self.solve_captcha()
        while self.captch_confidence < 0.9:
            time.sleep(captcha_sleep_time + random.uniform(-1, 1))
            print("Reloading CAPTCHA...")
            self.reload_captcha()
            self.get_captcha()
            self.solve_captcha()
        self.fill_captcha()
        self.check_handler()





def page_2():
    # Locate and click the desired link
    try:
        # link = driver.find_element(By.XPATH, "//a[contains(@onclick, 'startCommitRequest')]")
        link = driver.find_element(By.XPATH, "//a[contains(@onclick, 'startCommitRequest') and .//img[contains(@src, 'images/go-next.gif')]]")
        link.click()
        print("Clicked on the gonext successfully!")
    except Exception as e:
        print(f"Error: {e}")

    # Wait for the main form to load
    WebDriverWait(driver, general_wait_time).until(
        EC.presence_of_all_elements_located((By.NAME, "last_name"))
    )


def main_form():
    # Fill in the form fields
    driver.find_element(By.NAME, "lastname").send_keys(last_name)
    driver.find_element(By.NAME, "firstname").send_keys(first_name)
    driver.find_element(By.NAME, "email").send_keys(email)
    driver.find_element(By.NAME, "emailrepeat").send_keys(email)
    driver.find_element(By.NAME, "fields[0].content").send_keys(passport_number)
    driver.find_element(By.NAME, "fields[1].content").send_keys(phone_number)
    driver.find_element(By.NAME, "fields[2].content").send_keys(nationality)
    driver.find_element(By.NAME, "fields[3].content").send_keys(star_value)
    driver.find_element(By.NAME, "fields[4].content").send_keys(other_value)
    driver.find_element(By.NAME, "fields[5].content").send_keys(other_value)

    # Select checkboxes
    driver.find_element(By.NAME, "fields[6].content").click()
    driver.find_element(By.NAME, "fields[7].content").click()

    # CAPTCHA input (requires manual input or solving service)
    captcha_text = input("Enter CAPTCHA text from the image: ")
    driver.find_element(By.NAME, "captchaText").send_keys(captcha_text)

    # Submit the form
    driver.find_element(By.XPATH, "//input[@value='Submit']").click()








if __name__ == "__main__":

    # current_time = get_ntp_time()
    # print(f"Current time: {current_time}")

    # wait_until(start_time, sleep_interval=5)

    print("Starting...")


    # Setup Selenium WebDriver
    temp_dir = tempfile.mkdtemp()
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")  # Uncomment to run headless
    options.add_argument(f"--user-data-dir={temp_dir}")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)

    # Open the embassy appointment page
    driver.get(url)
    print("Page title: ", driver.title)


    page_1_ins = page_1(driver)
    page_1_ins.handle_page()
    raise SystemExit



    # Take screenshot (for debugging)
    driver.save_screenshot("confirmation.png")

    input("Press Enter to continue...")

    # Close browser
    driver.quit()


