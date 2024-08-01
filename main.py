import json
from game_links import get_deal_game_links, get_all_game_links, get_new_game_links, get_preorder_game_links
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

# get_preorder_game_links()
# get_deal_game_links()
# get_new_game_links()
# get_all_game_links()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

with open("data/games.json") as file:
    data = json.load(file)


@app.get("/games")
def get_game_links():
    with open("data/all_game_links.json") as file:
        data = json.load(file)
    return data


@app.get("/games/new")
def get_new_games():
    with open("data/deals_game_links.json") as file:
        data = json.load(file)
    return data


@app.get("/games/preorder")
def get_preorder_games():
    with open("data/preorder_game_links.json") as file:
        data = json.load(file)
    return data


@app.get("/games/deals")
def get_deal_games():
    with open("data/deals_game_links.json") as file:
        data = json.load(file)
    return data


@app.get("/games/{game_id}")
def get_game(game_id):
    return data[game_id]
