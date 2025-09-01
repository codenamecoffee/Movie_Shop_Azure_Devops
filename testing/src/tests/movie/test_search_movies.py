import os
import sys
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from src.models.requests.movie.movie_search_criteria import MovieSearchCriteria

class TestSearchMovies:

    @pytest.mark.smoke
    def test_search_a_movie_by_exact_name(self, movie_service, created_movie):
        search_name = created_movie["name"]
        criteria = MovieSearchCriteria(name=search_name)
        response = movie_service.search_movies(criteria=criteria, response_type=dict)
        movies_found = response.data

        assert response.status == 200 
        assert isinstance(movies_found, list)
        assert len(movies_found) > 0
        
        for movie in movies_found:
            assert "id" in movie 
            assert "name" in movie
            assert "director" in movie
            assert "genres" in movie
            assert "shop" in movie
            assert "rent" in movie
            
            assert isinstance(movie["id"], int) 
            assert isinstance(movie["name"], str) 
            assert isinstance(movie["director"], str)
            assert isinstance(movie["genres"], list)
            assert isinstance(movie["shop"], int)
            assert isinstance(movie["rent"], bool)
            
            assert movie["name"].lower() == search_name.lower()  
        
        movie_ids_found = [movie["id"] for movie in movies_found]
        assert created_movie["id"] in movie_ids_found

    @pytest.mark.smoke
    def test_search_a_movie_by_non_existent_name(self, movie_service):
        criteria = MovieSearchCriteria(
            name = "movie1Movie2Movie"
        )
        response = movie_service.search_movies(criteria=criteria, response_type=dict)
        movies_found = response.data

        assert response.status == 200 
        assert isinstance(movies_found, list)
        assert movies_found == []

    @pytest.mark.smoke
    def test_search_a_movie_by_exact_director(self, created_movie, movie_service):
        search_director = created_movie["director"]
        criteria = MovieSearchCriteria(director=search_director)
        response = movie_service.search_movies(criteria=criteria, response_type=dict)
        movies_found = response.data 

        assert response.status == 200  
        assert isinstance(movies_found, list)
        assert len(movies_found) > 0 
        
        for movie in movies_found:
            assert "id" in movie 
            assert "name" in movie
            assert "director" in movie
            assert "genres" in movie
            assert "shop" in movie
            assert "rent" in movie
            
            assert isinstance(movie["id"], int) 
            assert isinstance(movie["name"], str) 
            assert isinstance(movie["director"], str)
            assert isinstance(movie["genres"], list)
            assert isinstance(movie["shop"], int)
            assert isinstance(movie["rent"], bool)
    
            assert movie["director"].lower() == search_director.lower()
        
        movie_ids_found = [movie["id"] for movie in movies_found]
        assert created_movie["id"] in movie_ids_found

    @pytest.mark.smoke
    def test_search_a_movie_by_non_existent_director(self, movie_service):
        criteria = MovieSearchCriteria(
            director = "Mi perrito"
        )
        response = movie_service.search_movies(criteria=criteria, response_type=dict)
        movies_found = response.data
    
        assert response.status == 200 
        assert isinstance(movies_found, list)
        assert movies_found == [] 

    @pytest.mark.smoke
    def test_search_a_movie_by_exact_genre(self, movie_service, created_movie):
        search_genre = created_movie["genres"][0] 
        criteria = MovieSearchCriteria(genres=search_genre)
        response = movie_service.search_movies(criteria=criteria, response_type=dict)
        movies_found = response.data

        assert response.status == 200
        assert isinstance(movies_found, list)
        assert len(movies_found) > 0
        
        for movie in movies_found:
            assert "id" in movie
            assert "name" in movie
            assert "director" in movie
            assert "genres" in movie
            assert "shop" in movie
            assert "rent" in movie
        
            assert isinstance(movie["id"], int)
            assert isinstance(movie["name"], str)
            assert isinstance(movie["director"], str)
            assert isinstance(movie["genres"], list)
            assert isinstance(movie["shop"], int)
            assert isinstance(movie["rent"], bool)
            
            movie_genres_lower = [genre.lower() for genre in movie["genres"]]
            assert search_genre.lower() in movie_genres_lower
        
        movie_ids_found = [movie["id"] for movie in movies_found]
        assert created_movie["id"] in movie_ids_found

    @pytest.mark.smoke
    def test_search_a_movie_by_non_existent_genre(self, movie_service):
        criteria = MovieSearchCriteria(
            genres = "GeneroQueNoExiste2020"
        )
        response = movie_service.search_movies(criteria=criteria, response_type=dict)
        movies_found = response.data

        assert response.status == 200 
        assert isinstance(movies_found, list)
        assert movies_found == [] 

    @pytest.mark.smoke
    def test_search_a_movie_by_multiple_genres(self, movie_service, multi_genre_movie):
        criteria = MovieSearchCriteria(
            genres = ["Love", "Action", "Horror"]
        )
        response = movie_service.search_movies(criteria=criteria, response_type=dict)
        movies_found = response.data
        assert response.status == 200 
        assert isinstance(movies_found, list)
        assert len(movies_found) > 0 
        
        for movie in movies_found:
            assert "id" in movie
            assert "name" in movie
            assert "director" in movie
            assert "genres" in movie
            assert "shop" in movie
            assert "rent" in movie
            
            assert isinstance(movie["id"], int)
            assert isinstance(movie["name"], str)
            assert isinstance(movie["director"], str)
            assert isinstance(movie["genres"], list)
            assert isinstance(movie["shop"], int)
            assert isinstance(movie["rent"], bool)
        
            movie_genres_lower = [genre.lower() for genre in movie["genres"]] 
            
            for search_genre in criteria.genres: 
                assert search_genre.lower() in movie_genres_lower 

        movie_ids_found = [movie["id"] for movie in movies_found]
        assert multi_genre_movie["id"] in movie_ids_found

    @pytest.mark.smoke
    def test_search_a_movie_without_any_filter(self, movie_service, created_movie):
        criteria = MovieSearchCriteria()
        response = movie_service.search_movies(criteria=criteria,response_type=dict)
        movies_found = response.data
       
        assert response.status == 200 
        assert isinstance(movies_found, list)
        assert len(movies_found) > 0  
        
        for movie in movies_found:
            assert "id" in movie
            assert "name" in movie
            assert "director" in movie
            assert "genres" in movie
            assert "shop" in movie
            assert "rent" in movie
            
            assert isinstance(movie["id"], int)
            assert isinstance(movie["name"], str)
            assert isinstance(movie["director"], str)
            assert isinstance(movie["genres"], list)
            assert isinstance(movie["shop"], int)
            assert isinstance(movie["rent"], bool)
        
        movie_ids_found = [movie["id"] for movie in movies_found]
        assert created_movie["id"] in movie_ids_found