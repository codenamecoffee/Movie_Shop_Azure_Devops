import os

STATE_FILE = os.getenv("STATE_FILE", "app_state.json")
# Necesario para que la api en el contenedor funcione BIEN.

MOVIE_NOT_FOUND_MESSAGE = "Movie Not Found"
SHOP_NOT_FOUND_MESSAGE = "Shop Not Found"

MOVIE_ALREADY_RENTED = "Movie already rented"
MOVIE_NOT_RENTED = "Movie not rented"