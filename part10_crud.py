# a full example crud

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

class ItemIn(BaseModel):
    name : str
    price : float = Field(gt=0)

class ItemUpdate(BaseModel):
    name : str | None = None
    price : float | None = Field(default=None, gt=0)

class ItemOut(BaseModel):
    id : int 
    name : str
    price : float

items : dict[int, dict] = {}
next_id = 1

# create
@app.post('/items', response_model=ItemOut, status_code=201)
def create_item(item:ItemIn):
    global next_id
    new_item = {'id':next_id, **item.model_dump()}
    items[next_id] = new_item
    next_id += 1
    return new_item

# read all with a filter and paging 
@app.get('/items', response_model=list[ItemOut])
def list_items(search : str | None, max_price:float | None = None, skip:int = 0, limit:int = 10):
    result = list(items.values())
    if max_price is not None:
        result = [i for i in result if i["price"] <= max_price]
    if search is not None:
        result = [i for i in result if search.lower() in i['name'].lower()]
    return result[skip: skip + limit]

# read one
@app.get('/items/{item_id}', response_model=ItemOut)
def get_item(item_id : int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="item not found")
    return items[item_id]

# update part 
@app.patch('/items/{item_id}', response_model=ItemOut)
def update_item(item_id : int, changes : ItemUpdate):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")

    items[item_id].update(changes.model_dump(exclude_unset=True))

    return items[item_id]
# delete 
@app.delete('/items/{item_id}', status_code=204)
def delete_item(item_id : int):
    if item_id not in items: 
        raise HTTPException(status_code=404, detail="item not found")
    del items[item_id]


# put
@app.put('/items/{item_id}', response_model=ItemOut)
def replace_item(item_id : int, item : ItemIn):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="item not found")
    new_item = {'id':item_id, **item.model_dump}
    items[item_id] = new_item
    return new_item

    

