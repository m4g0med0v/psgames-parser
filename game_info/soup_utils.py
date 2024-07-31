from bs4 import BeautifulSoup

from fetch_utils import fetch_url

import json


def get_soup(href: str) -> BeautifulSoup:
    """
    Получает объект BeautifulSoup для указанного URL.

    Отправляет запрос по указанному URL, получает HTML-содержимое
    и парсит его с помощью BeautifulSoup.

    Args:
        href (str): URL страницы, которую нужно спарсить.

    Returns:
        BeautifulSoup: Объект BeautifulSoup, представляющий парсенное HTML-содержимое.
    """
    req = fetch_url(href)
    soup = BeautifulSoup(req, "html.parser")
    return soup


def find_script(data_name: str, soup: BeautifulSoup) -> dict:
    """
    Находит и извлекает JSON данные из script-тега в HTML-документе.

    Находит div с указанным значением атрибута data-mfe-name, затем находит script-тег
    с идентификатором, указанным в атрибуте data-initial этого div, и извлекает из него JSON данные.

    Args:
        data_name (str): Значение атрибута data-mfe-name для поиска div.
        soup (BeautifulSoup): Объект BeautifulSoup, представляющий HTML-документ.

    Returns:
        dict: Извлеченные JSON данные.

    Raises:
        KeyError: Если div или script не найдены, или отсутствует нужный атрибут.
        json.JSONDecodeError: Если содержимое script не является допустимым JSON.
    """
    # Получение div с указанным data-mfe-name
    div = soup.find("div", {"data-mfe-name": data_name})
    if div is None:
        raise KeyError(f"Div with data-mfe-name='{data_name}' not found.")

    # Получение script с идентификатором, указанным в data-initial
    script_id = div.get("data-initial")
    if script_id is None:
        raise KeyError(f"Div with data-mfe-name='{data_name}' does not have 'data-initial' attribute.")

    script = soup.find("script", {"id": script_id})
    if script is None:
        raise KeyError(f"Script with id='{script_id}' not found.")

    # Извлечение и возврат JSON данных
    return json.loads(script.text)
