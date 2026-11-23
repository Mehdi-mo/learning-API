from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI()

@app.get('/')
def home():
    return {'message': 'hello it works'}

@app.get('/items/{item_id}')
def get_item(item_id:int):
    return {'item_id': item_id}

@app.get('/items')
def list_items(limit: int = 10, category:str | None = None):
    return {'limit': limit, 'category': category}

@app.get('/square/{number}')
def squared(number: int):
    return {'square': number**2}

@app.get('/greet')
def greet(name : str, polite : bool = False):
    if polite : 
        return {'greeting': f'hi mr/ms {name}'}
    return {'greeting': f'hi {name}'}


class Item(BaseModel):
    name : str
    price : float = Field(gt=0)
    quantity : int = Field(default=1, ge=1)
    note : str | None = None

@app.post('/items')
def create_item(item:Item):
    total = item.price * item.quantity

    return {'name': item.name, 'total': total}
