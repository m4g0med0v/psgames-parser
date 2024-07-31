import json
from game_links import get_deal_game_links, get_all_game_links, get_new_game_links, get_preorder_game_links
from pathlib import Path
from game_info import PSClient
from fetch_utils import Fetch
from bs4 import BeautifulSoup
from configs import configure_logging
import logging


log = logging.getLogger(__name__)
configure_logging()


with open("data/all_game_links.json", "r") as file:
    data = json.load(file)
    log.info("ReadDB: Ссылки на все игры получены.")

data_path = Path("data/games.json")
if not data_path.exists():
    with open(data_path, "w") as file:
        file.write("{}")

browser = Fetch()

browser.open()
for item in data:
    with open(data_path, "r") as file:
        games = json.load(file)

    if games.get(item["id"]):
        log.info(f"Skip: Игра {item["name"]} присутствует в списке игр.")
        continue

    html = browser.get(item["url"])
    soup = BeautifulSoup(html, "html.parser")
    game = PSClient(soup)
    game_info = game.data()

    games[item["id"]] = game_info.model_dump()
    log.info(f"AddDB: Игра {item["name"]} добавлена.")

    with open(data_path, "w") as file:
        json.dump(games, file, indent=2)

browser.close()
