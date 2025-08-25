import os
import sys
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))


class TestSearchMovies:

    # C91
    @pytest.mark.smoke
    def test_search_a_movie_by_exact_name(self, movie_service, created_movie):
        
        # Nombre exacto de la movie que creamos:
        search_name = created_movie["name"]
        
        # Hacemos la consulta por nombre (search):
        response = movie_service.search_movies(name=search_name, response_type=dict)
        
        # Verificaciones básicas:
        assert response.status == 200  # Ok
        
        # Verificamos que devuelve una lista:
        movies_found = response.data # Más manipulable
        assert isinstance(movies_found, list)
        assert len(movies_found) > 0  # Al menos encontró la movie que creamos
        
        # Verificamos estructura válida de cada movie en la lista:
        for movie in movies_found:
            assert "id" in movie 
            assert "name" in movie
            assert "director" in movie
            assert "genres" in movie
            assert "shop" in movie
            assert "rent" in movie
            
            # Verificamos tipos de datos: 
            assert isinstance(movie["id"], int) 
            assert isinstance(movie["name"], str) 
            assert isinstance(movie["director"], str)
            assert isinstance(movie["genres"], list)
            assert isinstance(movie["shop"], int)
            assert isinstance(movie["rent"], bool)
            
            # Verificamos que el nombre coincide exactamente:
            assert movie["name"].lower() == search_name.lower()  # La api es case-INsensitive
        
        # Verificamos que nuestra movie creada está en los resultados:
        movie_ids_found = [movie["id"] for movie in movies_found]
        assert created_movie["id"] in movie_ids_found


    # C92
    @pytest.mark.smoke
    def test_search_a_movie_by_non_existent_name(self, movie_service):
        # Nombre inexistente:
        non_existent_name = "movie1Movie2Movie"
        
        # Hacemos la consulta por nombre inexistente:
        response = movie_service.search_movies(name=non_existent_name, response_type=dict)
        
        # Verificaciones:
        assert response.status == 200  # Ok (no es error, simplemente no hay resultados).
        
        # Verificamos que devuelve una lista vacía:
        movies_found = response.data
        assert isinstance(movies_found, list)
        assert movies_found == []  # lista vacía


    # C93
    @pytest.mark.smoke
    def test_search_a_movie_by_exact_director(self, created_movie, movie_service):
        # director exacto de la movie que creamos:
        search_director = created_movie["director"]
        
        # Hacemos la consulta por director (search):
        response = movie_service.search_movies(director=search_director, response_type=dict)
        
        # Verificaciones básicas:
        assert response.status == 200  # Ok
        
        # Verificamos que devuelve una lista:
        movies_found = response.data # Más manipulable.
        assert isinstance(movies_found, list)
        assert len(movies_found) > 0  # Al menos encontró la movie que creamos.
        
        # Verificamos estructura válida de cada movie en la lista:
        for movie in movies_found:
            assert "id" in movie 
            assert "name" in movie
            assert "director" in movie
            assert "genres" in movie
            assert "shop" in movie
            assert "rent" in movie
            
            # Verificamos tipos de datos: 
            assert isinstance(movie["id"], int) 
            assert isinstance(movie["name"], str) 
            assert isinstance(movie["director"], str)
            assert isinstance(movie["genres"], list)
            assert isinstance(movie["shop"], int)
            assert isinstance(movie["rent"], bool)
            
            # Verificamos que el nombre coincide exactamente:
            assert movie["director"].lower() == search_director.lower()  # La api es case-INsensitive
        
        # Verificamos que nuestra movie creada está en los resultados:
        movie_ids_found = [movie["id"] for movie in movies_found]
        assert created_movie["id"] in movie_ids_found



    # C94
    @pytest.mark.smoke
    def test_search_a_movie_by_non_existent_director(self, movie_service):
        # Director inexistente:
        non_existent_director = "Mi perrito"
        
        # Hacemos la consulta por nombre inexistente:
        response = movie_service.search_movies(director=non_existent_director, response_type=dict)
        
        # Verificaciones:
        assert response.status == 200  # Ok (no es error, simplemente no hay resultados).
        
        # Verificamos que devuelve una lista vacía:
        movies_found = response.data
        assert isinstance(movies_found, list)
        assert movies_found == []  # lista vacía.


    # C95
    @pytest.mark.smoke
    def test_search_a_movie_by_exact_genre(self, movie_service, created_movie):
        # Obtenemos el género de la movie que creamos:
        search_genre = created_movie["genres"][0]  # Tomamos el primer (y único) género.
        
        # Hacemos la consulta por género:
        response = movie_service.search_movies(genres=[search_genre], response_type=dict)
        
        # Verificaciones básicas:
        assert response.status == 200  # Ok
        
        # Verificamos que devuelve una lista:
        movies_found = response.data
        assert isinstance(movies_found, list)
        assert len(movies_found) > 0  # Al menos encontró la movie que creamos.
        
        # Verificamos estructura válida de cada movie en la lista:
        for movie in movies_found:
            assert "id" in movie
            assert "name" in movie
            assert "director" in movie
            assert "genres" in movie
            assert "shop" in movie
            assert "rent" in movie
            
            # Verificamos tipos de datos:
            assert isinstance(movie["id"], int)
            assert isinstance(movie["name"], str)
            assert isinstance(movie["director"], str)
            assert isinstance(movie["genres"], list)
            assert isinstance(movie["shop"], int)
            assert isinstance(movie["rent"], bool)
            
            # Verificamos que el género buscado está en los géneros de la movie:
            movie_genres_lower = [genre.lower() for genre in movie["genres"]]
            assert search_genre.lower() in movie_genres_lower
        
        # Verificamos que nuestra movie creada está en los resultados:
        movie_ids_found = [movie["id"] for movie in movies_found]
        assert created_movie["id"] in movie_ids_found


    # C98
    @pytest.mark.smoke
    def test_search_a_movie_by_non_existent_genre(self, movie_service):
        # Género que no existe:
        non_existent_genre = "GeneroQueNoExiste2020"
        
        # Hacemos la consulta por género inexistente:
        response = movie_service.search_movies(genres=[non_existent_genre], response_type=dict)
        
        # Verificaciones:
        assert response.status == 200  # Ok (no es error, simplemente no hay resultados).
        
        # Verificamos que devuelve una lista vacía:
        movies_found = response.data
        assert isinstance(movies_found, list)
        assert movies_found == []  # Lista vacía.


    # C96
    @pytest.mark.smoke
    def test_search_a_movie_by_multiple_genres(self, movie_service, multi_genre_movie):
        # Géneros a buscar (los mismos que tiene la movie del fixture):
        search_genres = ["Love", "Action", "Horror"]
        
        # Hacemos la consulta por múltiples géneros:
        response = movie_service.search_movies(genres=search_genres, response_type=dict)
        
        # Verificaciones básicas:
        assert response.status == 200  # Ok
        
        # Verificamos que devuelve una lista:
        movies_found = response.data
        assert isinstance(movies_found, list)
        assert len(movies_found) > 0  # Al menos encontró la movie que creamos.
        
        # Verificamos estructura válida de cada movie:
        for movie in movies_found:
            assert "id" in movie
            assert "name" in movie
            assert "director" in movie
            assert "genres" in movie
            assert "shop" in movie
            assert "rent" in movie
            
            # Tipos de datos:
            assert isinstance(movie["id"], int)
            assert isinstance(movie["name"], str)
            assert isinstance(movie["director"], str)
            assert isinstance(movie["genres"], list)
            assert isinstance(movie["shop"], int)
            assert isinstance(movie["rent"], bool)
        
            # La movie debe tener TODOS los géneros buscados (Recordar que SEGUIMOS en el for movie in movies_found):
            movie_genres_lower = [genre.lower() for genre in movie["genres"]] # Obtiene los genres de la movie en una lista.
            
            for search_genre in search_genres: # Para cada uno de los genres que mandamos en la consulta:
                assert search_genre.lower() in movie_genres_lower # Chequeamos si están en la lista de genres de la movie.

        # Verificamos que nuestra movie multi-género está en los resultados:
        movie_ids_found = [movie["id"] for movie in movies_found]
        assert multi_genre_movie["id"] in movie_ids_found



    # C97
    @pytest.mark.smoke
    def test_search_a_movie_without_any_filter(self, movie_service, created_movie):
        # Hacemos la consulta sin filtros (no enviamos name, director, ni genres):
        response = movie_service.search_movies(response_type=dict)
        
        # Verificaciones básicas:
        assert response.status == 200  # Ok
        
        # Verificamos que devuelve una lista:
        movies_found = response.data
        assert isinstance(movies_found, list)
        assert len(movies_found) > 0  # Debe devolver todas las movies existentes.
        
        # Verificamos estructura válida de cada movie:
        for movie in movies_found:
            assert "id" in movie
            assert "name" in movie
            assert "director" in movie
            assert "genres" in movie
            assert "shop" in movie
            assert "rent" in movie
            
            # Tipos de datos:
            assert isinstance(movie["id"], int)
            assert isinstance(movie["name"], str)
            assert isinstance(movie["director"], str)
            assert isinstance(movie["genres"], list)
            assert isinstance(movie["shop"], int)
            assert isinstance(movie["rent"], bool)
        
        # Verificamos que nuestra movie creada está en los resultados:
        movie_ids_found = [movie["id"] for movie in movies_found]
        assert created_movie["id"] in movie_ids_found

        # La movie de prueba ya existe desde el momento en que usamos 
        # created__movie["id"] en el assert.