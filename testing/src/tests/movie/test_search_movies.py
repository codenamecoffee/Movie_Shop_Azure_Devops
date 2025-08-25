import os
import sys
import pytest
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))


class TestSearchMovies:

    @pytest.mark.some
    def test_search_a_movie_by_exact_name(self):
        pass

    @pytest.mark.some
    def test_search_a_movie_by_non_existent_name(self):
        pass

    @pytest.mark.some
    def test_search_a_movie_by_exact_director(self):
        pass

    @pytest.mark.some
    def test_search_a_movie_by_non_existent_director(self):
        pass

    @pytest.mark.some
    def test_search_a_movie_by_exact_genre(self):
        pass