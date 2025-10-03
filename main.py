from typing import Union
import _sqlite3
from fastapi import FastAPI


app = FastAPI()


# Get aya by id
@app.get("/quran/ayas/{aya_id}")
def get_aya(aya_id: int):
    database = _sqlite3.connect("database/quran.db")
    cursor = database.cursor()
    cursor.execute("SELECT content FROM verses where id = (?)", (aya_id,))
    result = cursor.fetchall()
    database.close()
    return result

# Get ayas by page
@app.get("/quran/ayas/pages/{page}")
def get_aya_page(page: int):
    database = _sqlite3.connect("database/quran.db")
    cursor = database.cursor()
    cursor.execute("SELECT content FROM verses where page_id = (?)", (page,))
    result = cursor.fetchall()
    database.close()
    return result

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
