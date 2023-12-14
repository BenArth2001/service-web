from pydantic import BaseModel
from typing import List, Optional

class BaseOrmModel(BaseModel):
    class Config:
        orm_mode = True

class TradParams (BaseOrmModel):
    word: str
    dictionnary: str

class GetDico(BaseOrmModel):
    dictionnary: str

class SupprDicoLigne(BaseOrmModel):
    dictionnary: str
    line_key: str

class SupprDico(BaseOrmModel):
    dictionnary: str



class DicoLigne(BaseOrmModel):
    LineKey: str
    LineValue: str

class Dico(BaseOrmModel):
    name: str
    lines: List[DicoLigne] 

class MajDico(BaseOrmModel):
    nnom: Optional[str] = ...
    ncont: Optional[List[DicoLigne]]
