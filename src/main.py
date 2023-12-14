from http.client import HTTPException
from sqlite3 import IntegrityError
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from .params import TradParams, GetDico, SupprDico, SupprDicoLigne, DicoLigne, Dico, MajDico
from .response import IndexResponse, GetTradResponse, getDicoResponse, GetDicoResponse, postDicoResponse, DicoLineResponse, PostTradResponse, DeleteDico, DeleteDicoLine, MajDicoResponse
from .models import Trad, Base, Dictionnary, DictionnaryLine
from .database import SessionLocal, engine
from typing import List

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_model=IndexResponse)
def index():
    return {'msg': 'Rajouter /docs après cet URL pour arrivé dans la partie FAST API'}

@app.post("/trad", response_model=PostTradResponse)
def postTrad(params: TradParams, db: Session = Depends(get_db)):

    trad= "... --- ..."
    trad_db = Trad(word=params.word, trad=trad, dictionnary=params.dictionnary)
    db.add(trad_db)
    db.commit()

    return {
        'word': params.word,
        'dictionnary': params.dictionnary,
        'trad': trad
        }

#ANCIENNE METHODE SANS L'UTILISATION DE BASE DE DONNEE
# @app.get("/trad/{word}", response_model=getTradResponse)
# def trad(word : str):
#     morse_code = {'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
#                   'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
#                   'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
#                   'Y': '-.--', 'Z': '--..'}
#     newword = word.upper()
#     morse_translation = ''
#     for char in newword:
#         if char == ' ':
#             morse_translation += ' '
#         else:
#             morse_translation += morse_code.get(char, '')
#     return {
#         'word': morse_translation
#         }

# @app.get("/trad/{word}", response_model=GetTradResponse)
# def trad(word : str):
#     return {
#         'word' : word,
#     }


@app.get("/translate/")
def translate_word(word: str, dictionnary_name: str, db: Session = Depends(get_db)):
    #gd
    dictionnary = db.query(Dictionnary).filter(Dictionnary.name == dictionnary_name).first()

    if not dictionnary:
        raise HTTPException(status_code=404, detail="Dictionnary non trouvé")
    #gl
    lines = dictionnary.lines

    #T
    translated_word = ""
    for char in word:
        line = next((line for line in lines if line.lineKey == char), None)
        if line:
            translated_word += line.lineValue
        else:
            translated_word += char

    return {"word": word, "translated_word": translated_word}


@app.get("/dictionnaries/")
def read_all_dictionnaries(db: Session = Depends(get_db)):
    dictionnaries = db.query(Dictionnary).all()
    return dictionnaries


@app.delete("/dictionnaries/{dictionnary_id}")
def delete_dictionnary(dictionnary_id: int, db: Session = Depends(get_db)):
    dictionnary = db.query(Dictionnary).filter(Dictionnary.id == dictionnary_id).first()

    if not dictionnary:
        raise HTTPException(status_code=404, detail="Dico introuvable")

    db.delete(dictionnary)
    db.commit()

    return {"message": "Dico supprimé"}


@app.put("/update_dictionary/")
def update_dictionary(
    dictionnary_name: str,
    line_key: str,
    line_value: str,
    db: Session = Depends(get_db)
):
    #e?
    dictionnary = db.query(Dictionnary).filter(Dictionnary.name == dictionnary_name).first()

    if not dictionnary:
        #de?
        dictionnary = Dictionnary(name=dictionnary_name)
        db.add(dictionnary)
        db.commit()
        db.refresh(dictionnary)

    #le?
    existing_line = db.query(DictionnaryLine).filter(
        DictionnaryLine.dictionnary_id == dictionnary.id,
        DictionnaryLine.lineKey == line_key
    ).first()

    if existing_line:
        #le
        existing_line.lineValue = line_value
        db.commit()
        db.refresh(existing_line)
    else:
        #len
        new_line = DictionnaryLine(lineKey=line_key, lineValue=line_value, dictionnary_id=dictionnary.id)
        db.add(new_line)

        try:
            db.commit()
            db.refresh(new_line)
        except IntegrityError as e:
            #lKe
            db.rollback()
            raise HTTPException(status_code=400, detail="La line key existe déjà")

    return {"message": "Dico mit a jour"}

@app.get("/dictionary_lines/{dictionnary_name}")
def get_dictionary_lines(dictionnary_name: str, db: Session = Depends(get_db)):
    #de?
    dictionnary = db.query(Dictionnary).filter(Dictionnary.name == dictionnary_name).first()

    if not dictionnary:
        raise HTTPException(status_code=404, detail="Dico introuvable")

    #gal
    lines = db.query(DictionnaryLine).filter(DictionnaryLine.dictionnary_id == dictionnary.id).all()

    
    dictionary_lines = {line.lineKey: line.lineValue for line in lines}

    return {"dictionnary_name": dictionnary_name, "lines": dictionary_lines}

@app.delete("/delete_line/{dictionnary_name}/{line_key}")
def delete_line(dictionnary_name: str, line_key: str, db: Session = Depends(get_db)):
    #de?
    dictionnary = db.query(Dictionnary).filter(Dictionnary.name == dictionnary_name).first()

    if not dictionnary:
        raise HTTPException(status_code=404, detail="Dico introuvable")

    #lke?
    line = db.query(DictionnaryLine).filter(
        DictionnaryLine.dictionnary_id == dictionnary.id,
        DictionnaryLine.lineKey == line_key
    ).first()

    if not line:
        raise HTTPException(status_code=404, detail="Line key introuvable")

    #D
    db.delete(line)
    db.commit()

    return {"message": f"Line key '{line_key}' supprimé du dico '{dictionnary_name}'"}

@app.put("/change_dictionary_name/{old_name}/{new_name}")
def change_dictionary_name(old_name: str, new_name: str, db: Session = Depends(get_db)):
    #de?
    old_dictionary = db.query(Dictionnary).filter(Dictionnary.name == old_name).first()

    if not old_dictionary:
        raise HTTPException(status_code=404, detail="Dictionary not found")

    #no new
    new_dictionary = db.query(Dictionnary).filter(Dictionnary.name == new_name).first()

    if new_dictionary:
        raise HTTPException(status_code=400, detail="Dictionary with the new name already exists")

    #U
    old_dictionary.name = new_name
    db.commit()

    return {"message": f"Dico nom changé de '{old_name}' a '{new_name}'"}

@app.post("/create_dictionary/{name}")
def create_dictionary(name: str, db: Session = Depends(get_db)):
    #dn?
    existing_dictionary = db.query(Dictionnary).filter(Dictionnary.name == name).first()

    if existing_dictionary:
        raise HTTPException(status_code=400, detail="Dico exist deja")

    #C
    new_dictionary = Dictionnary(name=name)
    db.add(new_dictionary)
    db.commit()
    db.refresh(new_dictionary)

    return {"message": f"Dico '{name}' cree"}