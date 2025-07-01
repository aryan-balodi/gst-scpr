from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

def fetch_gstins(pan_number):
    try:
        # Set Chrome options
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")

        # Use system chromedriver
        driver = webdriver.Chrome(options=options)

        driver.get("https://services.gst.gov.in/services/searchtpbypan")
        print("Page loaded successfully")

        # Wait for the PAN input field
        pan_field = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "for_gstin"))
        )
        pan_field.clear()

        # Type PAN number slowly
        for char in pan_number:
            pan_field.send_keys(char)
            time.sleep(0.1)
        print(f"PAN entered: {pan_number}")

        # Manual CAPTCHA handling
        print("Please solve the CAPTCHA manually in the browser window")
        input("After entering CAPTCHA, press Enter here to continue...")

        # Wait a moment for any page updates after CAPTCHA entry
        time.sleep(1)

        # Click search button using correct ID from your screenshot
        search_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "lotsearch"))
        )
        search_btn.click()
        print("Search button clicked successfully")

        # Wait for results to load
        print("Waiting for results...")
        try:
            # Wait for either results table or error message
            WebDriverWait(driver, 30).until(
                EC.any_of(
                    EC.presence_of_element_located((By.CLASS_NAME, "table")),
                    EC.presence_of_element_located((By.CLASS_NAME, "alert")),
                    EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'Details')]")),
                    EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'No records')]"))
                )
            )
            print("Results loaded successfully")
        except:
            print("Results may have loaded but couldn't detect specific elements")

        # Save screenshot of results
        driver.save_screenshot("gst_results.png")
        print("Screenshot saved as gst_results.png")

        # Keep browser open for manual verification
        input("Press Enter to close the browser...")

    except Exception as e:
        print(f"Error: {str(e)}")
        if 'driver' in locals():
            driver.save_screenshot("error_screenshot.png")
            print("Error screenshot saved as error_screenshot.png")
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    pan_number = input("Enter PAN number: ").strip().upper()
    fetch_gstins(pan_number)
