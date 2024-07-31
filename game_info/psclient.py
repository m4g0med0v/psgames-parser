from datetime import datetime
from typing import Any, Dict, List, Tuple

from soup_utils import get_soup, find_script
from game_model import Game

import re


class URLError(Exception):
    pass


class PSClient:
    def __init__(self, href: str, id: str = None) -> None:
        """
        Класс PSClient для получения и парсинга данных о играх из магазина PlayStation.

        Аргументы:
        - href (str): URL страницы игры в магазине PlayStation.
        - id (str, опционально): ID игры (по умолчанию None).

        Атрибуты:
        - href (str): URL страницы игры в магазине PlayStation.
        - id (str): ID игры.
        - soup: Спарсенный HTML контент страницы игры.
        - product_id: Кортеж, представляющий тип и ID продукта/концепции.

        Методы:
        - __define_product_id(data): Определяет и возвращает тип и ID продукта или концепции игры.
        - __get_image(): Получает изображения, связанные с игрой.
        - __get_title(): Получает информацию о названии, включая имя, издателя, дату выпуска и т.д.
        - __get_price(): Получает информацию о цене игры.
        - __get_content_rating(): Получает данные о возрастном рейтинге, включая дескрипторы и интерактивные элементы.
        - __get_info(): Получает дополнительную информацию, такую как жанры, языки и описания.
        - __load(): Загружает и инициализирует данные из предоставленного URL страницы игры.
        - data(): Получает все необходимые данные и возвращает их в виде объекта Game.
        """

        self.href = href
        self.id = id
        self.soup = None
        self.product_id = None

    def __define_product_id(self, data) -> str:
        """
        Определяет и возвращает тип и ID продукта или концепции игры на основе входных данных.

        Аргументы:
        - data: Входные данные, содержащие соответствующую информацию об игре.

        Возвращает:
        - Кортеж: Тип ("product" или "concept") и ID игрового объекта.
        """

        if data["args"].get("productId"):
            product_id = data["args"]["productId"]
            return ("product", f"Product:{product_id}")
        else:
            concept_id = data["args"]["conceptId"]
            if data["cache"][f"Concept:{concept_id}"].get("defaultProduct"):
                return (
                    "product",
                    data["cache"][f"Concept:{concept_id}"]["defaultProduct"]["__ref"],
                )
            else:
                return ("concept", f"Concept:{concept_id}")

    def __get_image(self) -> List[Tuple]:
        """
        Получает изображения, связанные с игрой.

        Возвращает:
        - List[Tuple]: Список кортежей, содержащих роль изображения и URL.
        """

        image_data = find_script("gameBackgroundImage", self.soup)
        image = [
            (item["role"], item["url"])
            for item in image_data["cache"][self.product_id[1]]["media"]
        ]

        return image

    def __get_title(self) -> Dict[str, Any]:
        """
        Получает информацию о названии, включая имя, издателя, дату выпуска и т.д.

        Возвращает:
        - Dict[str, Any]: Словарь, содержащий детали названия.
        """

        title_data = find_script("gameTitle", self.soup)
        if self.product_id[0] == "product":
            title_product = title_data["cache"][self.product_id[1]]
            title = {
                "edition": (
                    title_product["edition"]["name"]
                    if title_product["edition"]
                    else None
                ),
                "name": title_product["name"],
                "platforms": title_product["platforms"],
                "publisher": title_product["publisherName"],
                "release": title_product["releaseDate"],
                "star_rating": {
                    "rating": title_product["starRating"]["averageRating"],
                    "count": title_product["starRating"]["totalRatingsCount"],
                },
                "category": title_product["topCategory"],
            }
        else:
            title_concept = title_data["cache"][self.product_id[1]]
            title = {
                "name": title_concept["name"],
                "publisher": title_concept["publisherName"],
                "release": title_concept["releaseDate"]["value"],
            }

        return title

    def __get_price(self) -> List:
        """
        Получает информацию о цене игры.

        Возвращает:
        - List: Список деталей о ценах.
        """

        price_data = find_script("ctaWithPrice", self.soup)
        price = []
        if self.product_id[0] == "product":
            price_product = price_data["cache"][self.product_id[1]]
            for game_cta in price_product["webctas"]:
                price.append(
                    {
                        "type": price_data["cache"][game_cta["__ref"]]["type"],
                        "info": price_data["cache"][game_cta["__ref"]]["price"],
                    }
                )
                del price[-1]["info"]["__typename"]
        else:
            price_concept = price_data["cache"][self.product_id[1]]
            price.append({"is_announce": price_concept["isAnnounce"]})

        return price

    def __get_content_rating(self) -> Dict[str, Any]:
        """
        Получает данные о возрастном рейтинге, включая дескрипторы и интерактивные элементы.

        Возвращает:
        - Dict[str, Any]: Словарь, содержащий детали возрастного рейтинга.
        """

        try:
            content_rating_data = find_script("contentRating", self.soup)
        except KeyError:
            return None

        rating = content_rating_data["cache"][self.product_id[1]]["contentRating"]
        content_rating = {
            "name": rating["description"],
            "image": rating["url"],
            "interactive_elements": [
                item.get("description") for item in rating["interactiveElements"]
            ],
            "descriptors": [item.get("description") for item in rating["descriptors"]],
        }

        return content_rating

    def __get_info(self) -> Dict[str, Any]:
        """
        Получает дополнительную информацию, такую как жанры, языки и описания.

        Возвращает:
        - Dict[str, Any]: Словарь, содержащий дополнительную информацию.
        """

        info_data = find_script("gameInfo", self.soup)
        if self.product_id[0] == "product":
            info_product = info_data["cache"][self.product_id[1]]
            info = {
                "genres": (
                    [item["value"] for item in info_product["localizedGenres"]]
                    if info_product["localizedGenres"]
                    else None
                ),
                "publisher": info_product["publisherName"],
                "release": info_product["releaseDate"],
                "spoken_languages": info_product["spokenLanguages"],
                "screen_languages": info_product["screenLanguages"],
                "platforms": info_product["platforms"],
                "description": [
                    (
                        item["type"],
                        item["value"].replace("<br>", "\n").replace("<br/>", "\n"),
                    )
                    for item in info_product["descriptions"]
                ],
                "type": info_product["type"],
            }
        else:
            info_concept = info_data["cache"][self.product_id[1]]
            info = {
                "genres": (
                    [item["value"] for item in info_concept["localizedGenres"]]
                    if info_concept["localizedGenres"]
                    else None
                ),
                "publisher": info_concept["publisherName"],
                "release": info_concept["releaseDate"]["value"],
                "description": [
                    (
                        item["type"],
                        item["value"].replace("<br>", "\n").replace("<br/>", "\n"),
                    )
                    for item in info_concept["descriptions"]
                ],
            }

        return info

    def __load(self) -> None:
        """
        Загружает и инициализирует данные из предоставленного URL страницы игры.
        Вызывает URLError, если предоставлен неверный URL.
        """

        if re.match(
            r"https://store.playstation.com/\w{2}-\w{2}/concept|https://store.playstation.com/\w{2}-\w{2}/product",
            self.href,
        ):
            self.soup = get_soup(self.href)
            self.product_id = self.__define_product_id(
                find_script("gameBackgroundImage", self.soup)
            )

            if not self.id:
                if "concept" in self.href:
                    self.id = self.href.replace(
                        "https://store.playstation.com/en-us/concept/", ""
                    )
                else:
                    self.id = self.href.replace(
                        "https://store.playstation.com/en-us/product/", ""
                    )
        else:
            raise URLError("Введена неправильная ссылка.")

    def data(self) -> Game:
        """
        Получает все необходимые данные и возвращает их в виде объекта Game.

        Возвращает:
        - Game: Объект Game, содержащий полученные данные.
        """

        self.__load()

        return Game(
            id=self.id,
            product_id=self.product_id,
            href=self.href,
            image=self.__get_image(),
            title=self.__get_title(),
            price=self.__get_price(),
            content_rating=self.__get_content_rating(),
            info=self.__get_info(),
            info_date=datetime.now(),
        )
