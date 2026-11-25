# start from a small official Python image
FROM python:3.12-slim

# work inside this folder in the container
WORKDIR /app

# copy the library list first and install
COPY requirements-api.txt .
RUN pip install --no-cache-dir -r requirements-api.txt

# now copy the code
COPY movie_rating_api/ ./movie_rating_api/

# the app listens on this port
EXPOSE 8000

# what runs when the container starts
CMD ["uvicorn", "movie_rating_api.main:app", "--host", "0.0.0.0", "--port", "8000"]