import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


__all__ = ['find_sidebar', 'send_message']


def find_sidebar(driver):
    """Check the side bar with chats"""
    try:
        element = WebDriverWait(driver, 130).until(
            EC.presence_of_element_located((By.ID, "side"))
        )
    except:
        print("No sidebar found")
        driver.quit()
        
        
def send_message(driver, link, phone, logs):
    driver.get(link)
    try:
        element = WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//button[@aria-label=\"Send\"]"))
        )
        element.click()
        time.sleep(3)
        logs += 1

    except:
        print("\tNo enviado %d" % phone)

    return logs
