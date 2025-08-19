import os
import pytest
from src.models.responses.base.response import Response
from services import MovieService


@pytest.mark.smoke

def test_get_movie_by_id(movie_service, created_movie):
    movie_id = created_movie["id"]
    response = movie_service.get_movie_by_id(movie_id)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == movie_id
    assert data["name"] == "Matrix"
    assert data["director"] == "Wachowski"
    assert data["genres"] == ["sci-fi"]
    assert "shop" in data
    assert data["rent"] is False

'''
@pytest.mark.smoke
def test_sign_in_with_valid_credentials(auth_service):
    credentials = CredentialsModel(
        username=os.getenv("USER"), password=os.getenv("PASSWORD")
    )
    response = auth_service.sign_in(credentials)
    assert response.status == 200


def test_sign_in_with_wrong_username(auth_service):
    credentials = CredentialsModel(
        username="wrong_username", password=os.getenv("PASSWORD")
    )
    response = auth_service.sign_in(credentials)
    assert response.status == 200
    assert response.data["reason"] == "Bad credentials"


def test_sign_in_with_wrong_password(auth_service):
    credentials = CredentialsModel(
        username=os.getenv("USER"), password="wrong_password"
    )
    response = auth_service.sign_in(credentials)
    assert response.status == 200
    assert response.data["reason"] == "Bad credentials"
'''