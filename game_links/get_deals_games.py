from configs import configure_logging
from .get_game_links import get_game_links

from pathlib import Path
from time import time

import logging


log = logging.getLogger(__name__)
configure_logging()


def get_deal_game_links() -> None:
    log.info("Function: get_deals_games()")
    start_time = time()
    href = "https://store.playstation.com/en-us/category/b2d586f8-d4a1-4c45-8e23-27d580936d5b/"
    data_path = Path("data/deals_game_links.json")
    get_game_links(href, data_path)
    log.info(f"Successfully: {data_path.name} {(time() - start_time):.3f}sec")
