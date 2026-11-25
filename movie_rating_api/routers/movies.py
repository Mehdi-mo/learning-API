import os
from fastapi import APIRouter, HTTPException, Header, Depends
from movie_rating_api.schemas import MovieIn, MovieOut, RatingIn, StatsOut, Genre


router = APIRouter(prefix="/movies", tags=["movies"])

movies : dict[int, dict] = {}
ratings : dict[int, list[int]] = {}        # movie_id -> [4, 5, 3]
next_id = 1


def check_key(x_api_key:str = Header()):
    if x_api_key != os.environ['API_KEY']:
        raise HTTPException(status_code=401, detail="wrong API Key")


# create a movie
@router.post("", response_model=MovieOut, status_code=201)
def create_movie(movie:MovieIn):
    global next_id
    new_movie = {"id":next_id, **movie.model_dump()}
    movies[next_id] = new_movie
    ratings[next_id] = []
    next_id += 1
    return new_movie


# read all the movies, with filters and paging
@router.get("", response_model=list[MovieOut])
def list_movies(genre : Genre | None = None, min_year : int | None = None,
                skip : int = 0, limit : int = 10):
    result = list(movies.values())
    if genre is not None:
        result = [m for m in result if m["genre"] == genre]
    if min_year is not None:
        result = [m for m in result if m["year"] >= min_year]
    return result[skip: skip + limit]


# read one movie
@router.get("/{movie_id}", response_model=MovieOut)
def get_movie(movie_id : int):
    if movie_id not in movies:
        raise HTTPException(status_code=404, detail="movie not available")
    return movies[movie_id]


# add a rating to one movie
@router.post("/{movie_id}/ratings", response_model=StatsOut, status_code=201)
def add_rating(movie_id : int, rating : RatingIn):
    if movie_id not in movies:
        raise HTTPException(status_code=404, detail="movie not available")
    ratings[movie_id].append(rating.value)
    return movie_stats(movie_id)


# how many ratings and the average
@router.get("/{movie_id}/stats", response_model=StatsOut)
def movie_stats(movie_id : int):
    if movie_id not in movies:
        raise HTTPException(status_code=404, detail="movie not available")

    scores = ratings[movie_id]
    if not scores:
        return {"count": 0, "average": None}

    return {"count": len(scores), "average": round(sum(scores) / len(scores), 2)}


# delete a movie, needs the API key
@router.delete('/{movie_id}', status_code=204, dependencies=[Depends(check_key)])
def delete_movie(movie_id : int):
    if movie_id not in movies:
        raise HTTPException(status_code=404, detail="movie not available")
    del movies[movie_id]
    del ratings[movie_id]