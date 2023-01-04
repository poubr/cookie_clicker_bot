from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time


# Setting up the driver
chrome_driver_path = "/Users/pavla/Development/chromedriver"
driver_service = Service(executable_path=chrome_driver_path)
driver = webdriver.Chrome(service=driver_service)

cookie_url = "http://orteil.dashnet.org/experiments/cookie/"
driver.get(cookie_url)


# Storing the most used objects
cookie = driver.find_element(By.ID, "cookie")
money = driver.find_element(By.ID, "money")
store = driver.find_element(By.ID, "store")


# Pause: When to check for purchase (10 seconds)
# End: When to end the game (5 minutes)
pause = time.time() + 5
end = time.time() + 300

while time.time() <= end:
    cookie.click()

    # If 5 seconds have passed:
    if time.time() > pause:

        # Find all items available for purchase (if there are any) and their prices
        for_purchase = store.find_elements(By.CSS_SELECTOR, "div :not(.grayed) > b")
        if len(for_purchase) > 0:
            available_items = {}
            available_funds = int(money.text.replace(",", ""))
            for item in for_purchase:
                available_items[item.text.split(" - ")[0]] = int(item.text.split(" - ")[1].replace(",", ""))

            # Find which item we can afford and which one is the most expensive one
            most_expensive_item = ""
            most_expensive_price = 0
            for item, price in available_items.items():
                if available_funds >= price:
                    if price > most_expensive_price:
                        most_expensive_item = item
                        most_expensive_price = price

            # Get the actual object to buy and clicking on it
            to_buy = driver.find_element(By.XPATH, f"//b[(text()='{most_expensive_item} - ')]")
            to_buy.click()
            print(f"Purchased {most_expensive_item} for {most_expensive_price}.")
            print("-----------------------------------------")

        else:
            print("Not enough funds for a purchase.")

        # Add another ten seconds for the next pause
        pause = time.time() + 5


# Checking how fast the cookies were made:
cps = driver.find_element(By.CSS_SELECTOR, "#cps")
print(cps.text)
cookies_per_second = cps.text.split(" : ")[1]
print(f"Final speed: {cookies_per_second} cookies per second.")


driver.quit()
