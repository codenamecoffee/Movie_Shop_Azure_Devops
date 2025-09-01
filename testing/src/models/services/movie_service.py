from typing import Type
from src.base.service_base import ServiceBase
from src.models.responses.base.response import T, Response
from src.models.requests.movie.movie_search_criteria import MovieSearchCriteria


class MovieService(ServiceBase):
    def __init__(self, base_url: str = ""):
        super().__init__("movies", base_url=base_url)

    def get_movies(self,  response_type: Type[T], config: dict | None = None) -> Response[T]:
        config = config or self.default_config
        return self.get(
            f"{self.url}",
            config=config,
            response_model=response_type,
        )
       
    def get_movie_by_id(self, movie_id: int, response_type: Type[T], config: dict | None = None) -> Response[T]:
        config = config or self.default_config
        return self.get(
            f"{self.url}/{movie_id}",
            config=config,
            response_model=response_type,
        )
    
    def create_movie(self, shop_id: int, movie_data: dict, response_type: Type[T] = None, config: dict | None = None) -> Response[T]:
        config = config or self.default_config
        url = f"{self.base_url}/shops/{shop_id}/movies"
        return self.post(
            url,
            data=movie_data,
            config=config,
            response_model=response_type,
        )
    
    def delete_movie(self, movie_id: int, response_type: Type[T] = None, config: dict | None = None) -> Response[T]:
        config = config or self.default_config
        return self.delete(
            f"{self.url}/{movie_id}",
            config=config,
            response_model=response_type,
        )
    
    def update_movie(self, movie_id: int, movie_data: dict, response_type: Type[T] = None, config: dict | None = None) -> Response[T]:
        config = config or self.default_config
        url = f"{self.base_url}/movies/{movie_id}"
        return self.put(
            url,
            data=movie_data,
            config=config,
            response_model=response_type,
        )
    
    def change_shop_movie(self, movie_id: int, shop_id: int, response_type: Type[T] = None, config: dict | None = None) -> Response[T]:
        config = config or self.default_config
        url = f"{self.base_url}/movies/{movie_id}/change-shop"
        data = {"shop_id": shop_id}
        return self.patch(
            url,
            data=data,
            config=config,
            response_model=response_type
        )

    def rent_movie(self, movie_id: int, response_type: Type[T] = None, config: dict | None = None) -> Response[T]:
        config = config or self.default_config
        url = f"{self.base_url}/movies/{movie_id}/rent-movie"
        return self.put(
            url,
            config=config,
            response_model=response_type
    )

    def return_movie(self, movie_id: int, response_type: Type[T] = None, config: dict | None = None) -> Response[T]:
        config = config or self.default_config
        url = f"{self.base_url}/movies/{movie_id}/return-movie"
        return self.put(
            url,
            config=config,
            response_model=response_type
        )

    def search_movies(self, criteria: MovieSearchCriteria, response_type: Type[T] = None, config: dict | None = None) -> Response[T]:
        config = config or self.default_config
        params = {}
        if criteria.name:
            params['name'] = criteria.name
        if criteria.director:
            params['director'] = criteria.director
        if criteria.genres:
            params['genres'] = criteria.genres

        url = f"{self.base_url}/movies/search"
        return self.get(
            url,
            params=params,
            config=config,
            response_model=response_type
        )
