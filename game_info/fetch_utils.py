from time import sleep

import random

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Настройки для Chrome
chrome_options = Options()
chrome_options.add_argument("--headless")  # Запуск в фоновом режиме
chrome_options.add_argument(
    "--disable-blink-features=AutomationControlled"
)  # Скрыть факт автоматизации
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
)


class FetchError(Exception):
    def __init__(self, message):
        super().__init__(message)


def fetch_url(url: str) -> str:
    """
    Загружает HTML-код страницы по указанному URL с использованием Selenium.

    Аргументы:
    url (str): URL-адрес веб-страницы для загрузки.

    Возвращает:
    str: HTML-код страницы в виде строки.
    """
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(url)
    browser.implicitly_wait(2)

    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(random.uniform(1, 3))

    html = browser.page_source
    browser.quit()
    return html


# def fetch_url(url: str, delay_interval: int = 3) -> str:
#     """
#     Получает HTML-содержимое страницы по указанному URL.

#     Отправляет GET-запрос по указанному URL с заданными заголовками.
#     В случае получения статуса 429 (Too Many Requests) повторяет попытку
#     через заданный интервал времени. В случае любого другого статуса,
#     отличного от 200, выбрасывает исключение FetchError.
#     Между запросами функция делает случайные паузы.

#     Args:
#         url (str): URL страницы, которую нужно загрузить.
#         delay_interval (int, optional): Интервал задержки в секундах
#             перед повторной попыткой при получении статуса 429. По умолчанию 3.

#     Returns:
#         str: HTML-содержимое страницы.

#     Raises:
#         FetchError: Если статус ответа не равен 200.
#     """
#     st_accept = "text/html"
#     st_useragent = UserAgent().chrome
#     headers = {
#         "Accept": st_accept,
#         "User-Agent": st_useragent,
#         "Referer": "https://www.google.com/",
#     }

#     response = requests.get(url, headers=headers)

#     if response.status_code == 429:
#         log.warning(
#             f"FetchError: {response.status_code}. Вы отправили слишком много запросов за определенное время."
#         )
#         log.info(f"Sleep: {delay_interval}sec")
#         sleep(delay_interval)
#         return fetch_url(url)
#     elif response.status_code != 200:
#         raise FetchError(
#             f"Error: {response.status_code}. Try a different proxy or user-agent"
#         )

#     sleep_time = random.uniform(1, 3)
#     sleep(sleep_time)

#     return response.text
