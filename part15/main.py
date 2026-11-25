from fastapi import FastAPI
from part15.routers import items

app = FastAPI(title="CRUD API")
app.include_router(items.router)
