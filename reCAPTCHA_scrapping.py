import os
from time import sleep, time
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

output_dir = './Google_captcha_images'
os.makedirs(output_dir, exist_ok=True)

DRIVER_PATH = './chromedriver'

num_images = 9000

options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)
url = 'https://www.google.com/recaptcha/api2/demo'

for i in range(6762, num_images):
    driver.get(url)

    # Move into the first iFrame (checkbox)
    driver.switch_to.frame(driver.find_elements(By.TAG_NAME, "iframe")[0])

    # Wait for checkbox to load
    checkBox = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "recaptcha-anchor"))
    )
    checkBox.click()

    # Move out of iFrame to main window
    driver.switch_to.default_content()
    sleep(12)

    captcha_frame = driver.find_elements(By.XPATH, "//iframe[@title='recaptcha challenge expires in two minutes']")

    for j, element in enumerate(captcha_frame):
        element_screenshot = element.screenshot_as_png
        output_image_path =os.path.join(output_dir, f"image_{i}.png")
        with open(output_image_path, "wb") as f:
            f.write(element_screenshot)

driver.quit()
