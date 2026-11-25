import os

# check_key reads this when a request comes in, so set it before any test runs
os.environ["API_KEY"] = "test-key"
API_KEY = "test-key"

from fastapi.testclient import TestClient
from movie_rating_api.main import app


def make_movie(client, name="Alien", genre="horror", year=1979):
    """create a movie and give back its id, so each test owns its own data"""
    r = client.post("/movies", json={"name": name, "genre": genre, "year": year})
    assert r.status_code == 201
    return r.json()["id"]


# ---------- create ----------

def test_create_movie():
    with TestClient(app) as client:
        r = client.post("/movies", json={"name": "Alien", "genre": "horror", "year": 1979})
        assert r.status_code == 201
        body = r.json()
        assert body["name"] == "Alien"
        assert body["genre"] == "horror"
        assert body["year"] == 1979
        assert "id" in body


def test_create_movie_bad_genre():
    with TestClient(app) as client:
        r = client.post("/movies", json={"name": "X", "genre": "drama", "year": 2000})
        assert r.status_code == 422


def test_create_movie_bad_year():
    with TestClient(app) as client:
        r = client.post("/movies", json={"name": "X", "genre": "action", "year": 100})
        assert r.status_code == 422


def test_create_movie_missing_field():
    with TestClient(app) as client:
        r = client.post("/movies", json={"name": "X"})
        assert r.status_code == 422


# ---------- list ----------

def test_list_movies():
    with TestClient(app) as client:
        movie_id = make_movie(client)
        r = client.get("/movies")
        assert r.status_code == 200
        ids = [m["id"] for m in r.json()]
        assert movie_id in ids


def test_list_filter_by_genre():
    with TestClient(app) as client:
        horror_id = make_movie(client, name="Alien", genre="horror", year=1979)
        action_id = make_movie(client, name="Heat", genre="action", year=1995)

        r = client.get("/movies", params={"genre": "horror", "limit": 100})
        ids = [m["id"] for m in r.json()]
        assert horror_id in ids
        assert action_id not in ids


def test_list_filter_by_min_year():
    with TestClient(app) as client:
        old_id = make_movie(client, name="Alien", genre="horror", year=1979)
        new_id = make_movie(client, name="Heat", genre="action", year=1995)

        r = client.get("/movies", params={"min_year": 1990, "limit": 100})
        ids = [m["id"] for m in r.json()]
        assert new_id in ids
        assert old_id not in ids


def test_list_bad_genre_filter():
    with TestClient(app) as client:
        r = client.get("/movies", params={"genre": "zzz"})
        assert r.status_code == 422


def test_list_paging():
    with TestClient(app) as client:
        make_movie(client)
        make_movie(client)
        r = client.get("/movies", params={"limit": 1})
        assert r.status_code == 200
        assert len(r.json()) == 1


# ---------- read one ----------

def test_get_movie():
    with TestClient(app) as client:
        movie_id = make_movie(client)
        r = client.get(f"/movies/{movie_id}")
        assert r.status_code == 200
        assert r.json()["name"] == "Alien"


def test_get_movie_not_found():
    with TestClient(app) as client:
        r = client.get("/movies/999999")
        assert r.status_code == 404


# ---------- ratings ----------

def test_stats_with_no_ratings():
    with TestClient(app) as client:
        movie_id = make_movie(client)
        r = client.get(f"/movies/{movie_id}/stats")
        assert r.status_code == 200
        assert r.json() == {"count": 0, "average": None}


def test_add_ratings_and_average():
    with TestClient(app) as client:
        movie_id = make_movie(client)
        client.post(f"/movies/{movie_id}/ratings", json={"value": 4})
        r = client.post(f"/movies/{movie_id}/ratings", json={"value": 5})

        assert r.status_code == 201
        assert r.json() == {"count": 2, "average": 4.5}


def test_add_rating_bad_value():
    with TestClient(app) as client:
        movie_id = make_movie(client)
        r = client.post(f"/movies/{movie_id}/ratings", json={"value": 9})
        assert r.status_code == 422


def test_add_rating_movie_not_found():
    with TestClient(app) as client:
        r = client.post("/movies/999999/ratings", json={"value": 4})
        assert r.status_code == 404


def test_stats_movie_not_found():
    with TestClient(app) as client:
        r = client.get("/movies/999999/stats")
        assert r.status_code == 404


# ---------- delete, protected by the key ----------

def test_delete_without_key():
    with TestClient(app) as client:
        movie_id = make_movie(client)
        r = client.delete(f"/movies/{movie_id}")
        assert r.status_code == 422          # the header itself is missing


def test_delete_with_wrong_key():
    with TestClient(app) as client:
        movie_id = make_movie(client)
        r = client.delete(f"/movies/{movie_id}", headers={"X-API-Key": "nope"})
        assert r.status_code == 401


def test_delete_with_right_key():
    with TestClient(app) as client:
        movie_id = make_movie(client)
        r = client.delete(f"/movies/{movie_id}", headers={"X-API-Key": API_KEY})
        assert r.status_code == 204

        # it is really gone
        assert client.get(f"/movies/{movie_id}").status_code == 404
        assert client.get(f"/movies/{movie_id}/stats").status_code == 404


def test_delete_movie_not_found():
    with TestClient(app) as client:
        r = client.delete("/movies/999999", headers={"X-API-Key": API_KEY})
        assert r.status_code == 404
