from fastapi import FastAPI
from movie_rating_api.routers import movies

app = FastAPI(title="movie rating api")
app.include_router(movies.router)
