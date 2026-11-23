from pydantic import BaseModel, Field
from fastapi import FastAPI
from typing import Literal


app = FastAPI()


class Student(BaseModel):
    name : str
    age : int = Field(ge=16, le=100)
    grade : Literal['A', 'B', 'C']

@app.post('/students')
def create_student(student: Student):
    return {**student.model_dump(), 'passed': student.grade in ['A', 'B']}



