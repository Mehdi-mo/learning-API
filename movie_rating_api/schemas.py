from pydantic import BaseModel, Field
from typing import Literal

Genre = Literal["horror", "slasher", "action", "comedy"]

class MovieIn(BaseModel):
    name : str 
    genre : Genre
    year : int = Field(ge=1888)
    

class MovieOut(BaseModel):
        id : int
        name : str 
        genre : Genre
        year : int
         

        
class RatingIn(BaseModel):
       value : int = Field(ge=1, le=5)


class StatsOut(BaseModel):
      count : int
      average : float | None = None