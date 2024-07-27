from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

class GoogleScraper:

    def __init__(self):
        self.PROXY_HOST = "45.127.248.127"
        self.PROXY_PORT = "5128"
        self.PROXY_USER = "nedylxcx"
        self.PROXY_PASS = "60xo02m57ubm"

        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36")
        self.chrome_options.add_argument(f'--proxy-server=http://{self.PROXY_HOST}:{self.PROXY_PORT}')
        self.driver = webdriver.Chrome(options=self.chrome_options)

        self.data = []

    def get_all(self, url):
        self.driver.maximize_window()
        self.driver.get(url)
        try:
            print(url)
            ## If user is on the overview tab, Then click on the More reviews button to goto reviews page.
            self.driver.find_element(By.XPATH, "//span[contains(text(), 'More reviews')]").click()
            time.sleep(2)
        except:
            pass

        data_container = WebDriverWait(self.driver, 5).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@class="m6QErb DxyBCb kA9KIf dS8AEf XiKgde "]')))
        num_of_scrolls = 0

        while True:
            current_reviews = len(self.driver.find_elements(By.CSS_SELECTOR, ".jJc9Ad"))
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', data_container)
            time.sleep(2)  # wait for the reviews to load

            new_num_loaded_reviews = len(self.driver.find_elements(By.CSS_SELECTOR, ".jJc9Ad"))
            if current_reviews == new_num_loaded_reviews: break

        total_reviews = self.driver.find_elements(By.CSS_SELECTOR, ".jJc9Ad")
        for review in total_reviews:
            avatar = review.find_element(By.CLASS_NAME, 'NBa7we').get_attribute('src')
            name = review.find_element(By.CLASS_NAME, 'd4r55').text
            stars = review.find_element(By.CLASS_NAME, 'kvMYJc')
            star_rating = stars.get_attribute('aria-label')  # Retrieve the aria-label attribute for the stars

            # Loop was breaking since some reviews didnt have comments so i placed this to keep the loop going.
            try:
                comment = review.find_element(By.CLASS_NAME, "wiI7pd").text
            except:
                comment = ''
            date_of_review = review.find_element(By.CLASS_NAME, "rsqaWe").text

            self.data.append({
                'hidden': 0,
                'user': name,
                'user_photo': avatar,
                'text': comment,
                'rating': star_rating,
                'highlight': None,
                'date': date_of_review,
                'reviewID': None,
                'reply': None
            })
        self.driver.quit()
        return self.data

    def get_eight_reviews(self, url):
        self.driver.maximize_window()
        self.driver.get(url)

        total_reviews = self.driver.find_elements(By.CSS_SELECTOR, ".jJc9Ad")
        for review in total_reviews:
            name = review.find_element(By.CLASS_NAME, 'd4r55').text
            stars = review.find_element(By.CLASS_NAME, 'kvMYJc')
            star_rating = stars.get_attribute('aria-label')  # Retrieve the aria-label attribute for the stars

            # Loop was breaking since some reviews didnt have comments so i placed this to keep the loop going.
            try:
                comment = review.find_element(By.CLASS_NAME, "wiI7pd").text
            except:
                comment = ''
            date_of_review = review.find_element(By.CLASS_NAME, "rsqaWe").text

            self.data.append({
                'name': name,
                'rating': star_rating,
                'comment': comment,
                'date_of_review': date_of_review
            })
        self.driver.quit()
        print(self.data)
        return self.data

