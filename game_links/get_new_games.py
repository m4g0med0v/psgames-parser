from configs import configure_logging
from game_links import get_game_links

from pathlib import Path
from time import time

import logging


log = logging.getLogger(__name__)
configure_logging()


def get_new_game_links() -> None:
    log.info("Function: get_new_games()")
    start_time = time()
    href = "https://store.playstation.com/en-us/category/e1699f77-77e1-43ca-a296-26d08abacb0f/"
    data_path = Path("data/new_game_links.json")
    get_game_links(href, data_path)
    log.info(f"Successfully: {data_path.name} {(time() - start_time):.3f}sec")
