from typing import Union
import _sqlite3
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get chapters
@app.get("/quran/chapters")
def get_chapters():
    f = open("database/surah.json", encoding='utf-8')
    data = json.load(f)
    f.close()
    return data

# Get aya by id
@app.get("/quran/ayas/{aya_id}")
def get_aya(aya_id: int):
    database = _sqlite3.connect("database/quran.db")
    cursor = database.cursor()
    cursor.execute("SELECT * FROM verses where id = (?)", (aya_id,))
    result = cursor.fetchall()
    database.close()
    return result

# Get ayas by page
@app.get("/quran/ayas/pages/{page}")
def get_aya_page(page: int):
    database = _sqlite3.connect("database/quran.db")
    database.row_factory = _sqlite3.Row
    cursor = database.cursor()

    cursor.execute("SELECT * FROM verses WHERE page_id = ?", (page,))
    rows = cursor.fetchall()

    result = [dict(row) for row in rows]
    database.close()

    return {"verses":result}

# Get tafsir by aya
@app.get("/quran/tafsir/{tafsir}/{aya_id}")
def get_tafsir(tafsir: int, aya_id: int):
    database = _sqlite3.connect("database/quran.db")
    cursor = database.cursor()
    if tafsir == 0: # Almysr
        cursor.execute("SELECT content FROM items where id = (?)", (aya_id,))
    elif tafsir == 1: # English
        cursor.execute("SELECT content FROM items where id = (?)", (aya_id+6236,))
    result = cursor.fetchall()
    database.close()
    return result
