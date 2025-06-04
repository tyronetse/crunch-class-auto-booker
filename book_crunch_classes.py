from datetime import datetime, timedelta
import pytz
import json
import time
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def read_credentials():
    with open("credentials.json") as f:
        return json.load(f)

def read_classes_to_book():
    with open("classes.json") as f:
        return json.load(f)

def launch_browser():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(options=chrome_options)

def login(driver, username, password):
    print("🌐 Opening login page...")
    driver.get("https://members.crunch.com/members/sign_in")
    try:
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "login-email")))
        WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "login-password")))

        print("🔐 Logging in...")
        driver.find_element(By.ID, "login-email").send_keys(username)
        driver.find_element(By.ID, "login-password").send_keys(password)
        driver.find_element(By.NAME, "commit").click()

        WebDriverWait(driver, 20).until(EC.url_contains("/members"))
        print("✅ Logged in successfully.")
        return True

    except TimeoutException:
        print("❌ Login timed out.")
        return False

def navigate_to_my_classes(driver):
    print("📄 Navigating to My Classes page...")
    driver.get("https://members.crunch.com/my-classes")

def click_day_tab(driver, target_day):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".weektabs-tab"))
        )
        day_tabs = driver.find_elements(By.CSS_SELECTOR, ".weektabs-tab")
        for tab in day_tabs:
            day_attr = tab.get_attribute("data-dayname")
            if day_attr and day_attr.strip().lower() == target_day.strip().lower():
                print(f"📆 Clicking tab for {day_attr}...")
                tab.click()
                time.sleep(2)
                return True
    except Exception as e:
        print(f"❌ Failed to click on the day tab: {e}")
    return False

def try_booking_class(driver, class_to_book):
    print("🔍 Looking for class button...")
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, ".class-detail, .schedules-row")))
        class_buttons = driver.find_elements(By.CSS_SELECTOR, ".class-detail, .schedules-row")

        for btn in class_buttons:
            if class_to_book["name"].lower() in btn.text.lower() and class_to_book["time"] in btn.text:
                try:
                    reserve_btn = btn.find_element(
                        By.XPATH,
                        ".//*[self::button or self::a][contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'reserve')]"
                    )
                    if reserve_btn.is_displayed() and reserve_btn.is_enabled():
                        print("🟢 Reserve button found, attempting to click...")
                        reserve_btn.click()
                        print("🎉 Class reserved successfully!")
                        return True
                    else:
                        print("⚠️ Reserve button is not clickable.")
                except Exception as e:
                    print(f"⚠️ Reserve button not found or error clicking: {e}")
                break
        print(f"❌ {class_to_book['name']} is not available (fully booked or reserve button missing).")
    except Exception as e:
        print(f"❌ Error booking class: {e}")
    return False

def main_loop():
    credentials = read_credentials()
    classes_to_book = read_classes_to_book()
    USERNAME = credentials["username"]
    PASSWORD = credentials["password"]

    tz = pytz.timezone("America/Chicago")
    print("🔁 Starting continuous booking loop. Press Ctrl+C to stop.")

    while True:
        now = datetime.now(tz)

        for class_to_book in classes_to_book:
            day = class_to_book["day"]
            time_str = class_to_book["time"]
            next_class_date = now + timedelta(days=(7 + (["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"].index(day.lower()) - now.weekday())) % 7)
            class_start_dt = tz.localize(datetime.combine(next_class_date.date(), datetime.strptime(time_str, "%I:%M %p").time()))
            booking_open_time = class_start_dt - timedelta(hours=22)
            earliest_login_time = booking_open_time - timedelta(minutes=5)

            print(f"📅 Class to book: {class_to_book}")
            print(f"⏳ Booking will happen at {booking_open_time.strftime('%A %I:%M %p')}")

            if earliest_login_time <= now <= class_start_dt:
                driver = launch_browser()
                try:
                    if not login(driver, USERNAME, PASSWORD):
                        driver.quit()
                        continue
                    navigate_to_my_classes(driver)
                    if not click_day_tab(driver, class_to_book["day"]):
                        print("❌ Could not click correct day tab.")
                        driver.quit()
                        continue
                    seconds_until_booking = (booking_open_time - datetime.now(tz)).total_seconds()
                    if seconds_until_booking > 0:
                        print(f"⏳ Waiting {int(seconds_until_booking)} seconds for booking to open...")
                        time.sleep(seconds_until_booking)

                    if try_booking_class(driver, class_to_book):
                        print(f"✅ Successfully booked {class_to_book['name']}")
                finally:
                    driver.quit()
        print("🔄 Loop complete. Sleeping for 5 minutes...")
        time.sleep(300)

main_loop()
