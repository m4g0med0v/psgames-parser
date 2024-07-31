from time import sleep

import random

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Fetch():
    def open(self) -> None:
        chrome_options = Options()  # Настройки для Chrome
        # chrome_options.add_argument("--headless")  # Запуск в фоновом режиме
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # Скрыть факт автоматизации
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--ignore-ssl-errors')
        self.browser = webdriver.Chrome(options=chrome_options)

    def get(self, url: str) -> str:
        self.browser.get(url)
        self.browser.implicitly_wait(5)
        sleep(random.uniform(2, 3))
        self.browser.execute_script(f"window.scrollTo(0, document.body.scrollHeight);")
        

        html = self.browser.page_source
        return html

    def close(self) -> None:
        self.browser.quit()
