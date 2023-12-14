from pydantic import BaseModel
from .params import DicoLigne
from typing import List

class BaseOrmModel(BaseModel):
    class Config:
        orm_mode = True

class IndexResponse(BaseOrmModel):
    msg: str

class GetTradResponse(BaseOrmModel):
    word: str
    dictionnary_id: int
    trad: str

class GetDicoResponse(BaseOrmModel):
    id : int
    lines : List[DicoLigne] = []
    name : str

class getDicoResponse(BaseOrmModel):
    id: int
    name: str
    lines: List[DicoLigne] = []

class postDicoResponse(BaseOrmModel):
    id : int
    name : str
    lines :  List[DicoLigne] = []

class DicoLineResponse(BaseOrmModel):
    id: int
    LineKey: str
    LineValue: str
    

class PostTradResponse(BaseOrmModel):
    word: str
    dictionnary: str
    trad: str

class DeleteDicoLine(BaseModel):
    message: str

class DeleteDico(BaseModel):
    message: str

class MajDicoResponse(BaseModel):
    message: str

    