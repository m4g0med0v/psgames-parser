from game_info import get_soup
from configs import configure_logging

from pathlib import Path

import logging
import json


log = logging.getLogger(__name__)
configure_logging()


def get_game_links(href: str, data_path: Path) -> None:
    ans = []

    # Цикл для прохода по всем страницам ссылки
    page = 1
    while True:
        # Получение html страницы
        soup = get_soup(f"{href}{page}")

        # Получаем элементы в которых хранятся ссылки на игры
        games = soup.select('div[id="__next"] > main[id="main"] ul li a')
        # div[id="__next"] > main[id="main"] ul li a div[data-qa^="ems-sdk-grid#productTile"] > section
        # type (none) div[id="__next"] > main[id="main"] ul li a div[data-qa^="ems-sdk-grid#productTile"] > section > span[data-qa$="product-type"]
        # discount-badge (none) div[id="__next"] > main[id="main"] ul li a div[data-qa^="ems-sdk-grid#productTile"] > section  span[data-qa$="discount-badge#text"]
        # display-price div[id="__next"] > main[id="main"] ul li a div[data-qa^="ems-sdk-grid#productTile"] > section  > div[data-qa$="price"] span[data-qa$="#price#display-price"]
        # discount-price div[id="__next"] > main[id="main"] ul li a div[data-qa^="ems-sdk-grid#productTile"] > section  > div[data-qa$="price"] s[data-qa$="#price#price-strikethrough"]
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
                }
            )

        log.info(f"Page: {page}")
        page += 1

    # Запись полученных ссылок игр в файл
    with open(data_path.absolute(), "w") as file:
        json.dump(ans, file, indent=2)
