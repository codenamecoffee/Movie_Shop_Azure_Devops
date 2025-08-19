import os, json
from typing import Dict
from src.schemas.schemas import Movie, Shop

def save_state(filename: str, movies: Dict[int, Movie], shops: Dict[int, Shop], next_movie_id: int, next_shop_id: int):
    data = {
        "movies": {k: v.model_dump() for k, v in movies.items()},
        "shops": {k: {
            "id": v.id,
            "address": v.address,
            "manager": v.manager,
            "movies": [m.id for m in v.movies]
        } for k, v in shops.items()},
        "next_movie_id": next_movie_id,
        "next_shop_id": next_shop_id
    }
    with open(filename, "w") as f:
        json.dump(data, f)

def load_state(filename: str):
    movies: Dict[int, Movie] = {}
    shops: Dict[int, Shop] = {}
    next_movie_id = 1
    next_shop_id = 1     
    if not os.path.exists(filename):
        return movies, shops, next_movie_id, next_shop_id
   
    with open(filename, "r") as f:
        data = json.load(f)
        # Load movies
        movies.clear()
        for k, v in data["movies"].items():
            movies[int(k)] = Movie(**v)
        # Load shops
        shops.clear()
        for k, v in data["shops"].items():
            shop_movies = [movies[mid] for mid in v["movies"] if mid in movies]
            shops[int(k)] = Shop(id=v["id"], address=v["address"], manager=v["manager"], movies=shop_movies)
        next_movie_id = data["next_movie_id"]
        next_shop_id = data["next_shop_id"]
    return movies, shops, next_movie_id, next_shop_id
