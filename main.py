import json
from game_links import get_deal_game_links, get_all_game_links, get_new_game_links, get_preorder_game_links


# with open("data/all_game_links.json", "r") as file:
#     data = json.load(file)


get_deal_game_links()
get_new_game_links()
get_preorder_game_links()
