import os
import sys
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from src.models.requests.movie.movie_search_criteria import MovieSearchCriteria
from src.models.responses.movie.movie_response import MovieResponse

class TestSearchMovies:

    @pytest.mark.smoke
    def test_search_a_movie_by_exact_name(self, movie_service, created_movie):
        search_name = created_movie["name"]
        criteria = MovieSearchCriteria(name=search_name)
        response = movie_service.search_movies(criteria=criteria, response_type=MovieResponse)
        movies_found = response.data
        movie_ids_found = [movie.id for movie in movies_found]
        assert response.status == 200 
        assert len(movies_found) > 0
        assert created_movie["id"] in movie_ids_found

        for movie in movies_found:
            assert movie.name.lower() == search_name.lower()

    @pytest.mark.smoke
    def test_search_a_movie_by_non_existent_name(self, movie_service):
        criteria = MovieSearchCriteria(
            name = "movie1Movie2Movie"
        )
        response = movie_service.search_movies(criteria=criteria, response_type=MovieResponse)

        assert response.status == 200 
        assert response.data == []

    @pytest.mark.smoke
    def test_search_a_movie_by_exact_director(self, created_movie, movie_service):
        search_director = created_movie["director"]
        criteria = MovieSearchCriteria(director=search_director)
        response = movie_service.search_movies(criteria=criteria, response_type=MovieResponse)
        movies_found = response.data
        movie_ids_found = [movie.id for movie in movies_found] 

        assert response.status == 200  
        assert len(movies_found) > 0 
        assert created_movie["id"] in movie_ids_found

        for movie in movies_found:
            assert movie.director.lower() == search_director.lower()
        
    @pytest.mark.smoke
    def test_search_a_movie_by_non_existent_director(self, movie_service):
        criteria = MovieSearchCriteria(
            director = "Mi perrito"
        )
        response = movie_service.search_movies(criteria=criteria, response_type=MovieResponse)

        assert response.status == 200 
        assert response.data == [] 

    @pytest.mark.smoke
    def test_search_a_movie_by_exact_genre(self, movie_service, created_movie):
        search_genre = created_movie["genres"][0] 
        criteria = MovieSearchCriteria(genres=[search_genre])
        response = movie_service.search_movies(criteria=criteria, response_type=MovieResponse)
        movies_found = response.data
        movie_ids_found = [movie.id for movie in movies_found]

        assert response.status == 200
        assert len(movies_found) > 0
        assert created_movie["id"] in movie_ids_found

        for movie in movies_found:        
            movie_genres_lower = [genre.lower() for genre in movie.genres]
            assert search_genre.lower() in movie_genres_lower
        
    @pytest.mark.smoke
    def test_search_a_movie_by_non_existent_genre(self, movie_service):
        criteria = MovieSearchCriteria(
            genres = ["GeneroQueNoExiste2020"]
        )
        response = movie_service.search_movies(criteria=criteria, response_type=MovieResponse)

        assert response.status == 200 
        assert response.data == [] 

    @pytest.mark.smoke
    def test_search_a_movie_by_multiple_genres(self, movie_service, multi_genre_movie):
        criteria = MovieSearchCriteria(
            genres = ["Love", "Action", "Horror"]
        )
        response = movie_service.search_movies(criteria=criteria, response_type=MovieResponse)
        movies_found = response.data
        movie_ids_found = [movie.id for movie in movies_found]

        assert response.status == 200 
        assert len(movies_found) > 0 
        assert multi_genre_movie["id"] in movie_ids_found
        
        for movie in movies_found:
            movie_genres_lower = [genre.lower() for genre in movie.genres] 
            
            for search_genre in criteria.genres: 
                assert search_genre.lower() in movie_genres_lower 

    @pytest.mark.smoke
    def test_search_a_movie_without_any_filter(self, movie_service, created_movie):
        criteria = MovieSearchCriteria()
        response = movie_service.search_movies(criteria=criteria,response_type=MovieResponse)
        movies_found = response.data
        movie_ids_found = [movie.id for movie in movies_found]
       
        assert response.status == 200 
        assert len(movies_found) > 0  
        assert created_movie["id"] in movie_ids_found
    
        
        
        