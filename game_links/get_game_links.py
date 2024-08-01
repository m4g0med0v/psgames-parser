from configs import configure_logging
from fetch_utils import Fetch

from bs4 import BeautifulSoup
from pathlib import Path

import logging
import json


log = logging.getLogger(__name__)
configure_logging()


def get_game_links(href: str, data_path: Path) -> None:
    ans = []
    browser = Fetch()

    # Открываем брузер
    browser.open()

    # Цикл для прохода по всем страницам ссылки
    page = 1
    while True:
        # Получение html страницы
        html = browser.get(f"{href}{page}")
        soup = BeautifulSoup(html, "html.parser")

        # Получаем элементы в которых хранятся ссылки на игры
        games = soup.select('div[id="__next"] > main[id="main"] ul li a')

        # Если на странице нет игр цикл заканчивается
        if not games:
            break

        # Прохожимся по всем элементам и получаем данные
        for item in games:
            data_json = json.loads(item["data-telemetry-meta"])
            ans.append(
                {
                    "id": data_json["id"],
                    "name": data_json["name"],
                    "url": f"https://store.playstation.com{item["href"]}",
                    "image": soup.select_one(f'div[id="__next"] > main[id="main"] ul li a img[data-qa$="#productTile{data_json["index"]}#game-art#image#image"]')["src"][:-6]
                }
            )

        log.info(f"Page: {page}")
        page += 1

    # Закрываем браузер
    browser.close()

    # Запись полученных ссылок игр в файл
    with open(data_path.absolute(), "w") as file:
        json.dump(ans, file, indent=2)
