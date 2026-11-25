from pydantic import BaseModel, Field


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