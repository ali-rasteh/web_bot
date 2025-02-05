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



manual_captcha = True


# url = "https://service2.diplo.de/rktermin/extern/appointment_showMonth.do?locationCode=tehe&realmId=22&categoryId=3069"  # Adjust path if necessary
url = "file:///C:/Users/alira/OneDrive/Desktop/Current_works/web_bot/form_main.html"
# start_time = "2025-02-12 02:30:01 UTC"
start_time = "08:35:01"
# time_format = "%Y-%m-%d %H:%M:%S %z"


last_name = "Rasteh"
first_name = "Vahid"
email = "vahid.rasteh0@gmail.com"
passport_number = "A12345678"
phone_number = "+1234567890"
nationality = "Iran"
star_value = '1'
other_value = '-'





if manual_captcha == False:
    import pytesseract
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    import base64
    from PIL import Image
    import io



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
    

def page_1():
    # Locate CAPTCHA Image (Base64)
    captcha_element = driver.find_element(By.XPATH, "//div[contains(@style, 'background:white url')]")
    captcha_style = captcha_element.get_attribute("style")

    # Extract Base64 CAPTCHA data
    base64_start = "data:image/jpg;base64,"
    start_index = captcha_style.find(base64_start) + len(base64_start)
    end_index = captcha_style.find("')", start_index)
    captcha_base64 = captcha_style[start_index:end_index]
    # print(f"Extracted CAPTCHA Base64: {captcha_base64}...")


    if manual_captcha:
        # captcha_image.show()
        captcha_text = input("Please enter the CAPTCHA text displayed: ").strip()
    else:
        # Decode Base64 and save CAPTCHA image
        captcha_bytes = base64.b64decode(captcha_base64)
        captcha_image = Image.open(io.BytesIO(captcha_bytes))
        captcha_image.save("captcha.png")

        # Use OCR to extract text
        captcha_text = pytesseract.image_to_string(captcha_image, config='--psm 6').strip()
        print(f"Extracted CAPTCHA text: {captcha_text}")

    # Fill in the CAPTCHA text
    captcha_input = driver.find_element(By.ID, "appointment_captcha_month_captchaText")
    captcha_input.send_keys(captcha_text)

    # Submit the form
    submit_button = driver.find_element(By.ID, "appointment_captcha_month_appointment_showMonth")
    submit_button.click()
    print("CAPTCHA submitted successfully!")

    # Wait for new page to load by checking a known element on Page 2
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(@onclick, 'startCommitRequest') and .//img[contains(@src, 'images/go-next.gif')]]"))
    )
    print("Page 2 loaded successfully!")


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
    WebDriverWait(driver, 10).until(
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

    current_time = get_ntp_time()
    print(f"Current time: {current_time}")

    wait_until(start_time, sleep_interval=5)

        
    raise SystemExit
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


    # page_1()
    # page_2()
    main_form()



    # Take screenshot (for debugging)
    driver.save_screenshot("confirmation.png")

    input("Press Enter to continue...")

    # Close browser
    driver.quit()


