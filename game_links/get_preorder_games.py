from configs import configure_logging
from .get_game_links import get_game_links

from pathlib import Path
from time import time

import logging


log = logging.getLogger(__name__)
configure_logging()


def get_preorder_game_links() -> None:
    log.info("Function: get_preorder_games()")
    start_time = time()
    href = "https://store.playstation.com/en-us/category/3bf499d7-7acf-4931-97dd-2667494ee2c9/"
    data_path = Path("data/preorder_game_links.json")
    get_game_links(href, data_path)
    log.info(f"Successfully: {data_path.name} {(time() - start_time):.3f}sec")
