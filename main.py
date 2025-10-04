from typing import Union
import _sqlite3
import json
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
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
def get_aya(aya_id: str):
    database = _sqlite3.connect("database/quran.db", check_same_thread=False)
    cursor = database.cursor()
    cursor.execute("SELECT * FROM verses WHERE verse_key = ?", (aya_id,))
    rows = cursor.fetchall()
    result = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
    database.close()
    return {"verses": result}


# Get ayas by page
@app.get("/quran/ayas/pages/{page}")
def get_aya_page(page: int):
    database = _sqlite3.connect("database/quran.db", check_same_thread=False)
    database.row_factory = _sqlite3.Row
    cursor = database.cursor()

    cursor.execute("SELECT * FROM verses WHERE page_id = ?", (page,))
    rows = cursor.fetchall()

    result = [dict(row) for row in rows]
    database.close()

    return {"verses":result}

# Get tafsir by aya
@app.get("/quran/tafsir/{tafsir}/{aya_id}")
def get_tafsir(tafsir: int, aya_id: str):
    try:
        database = _sqlite3.connect("database/tafsir.db", check_same_thread=False)
        cursor = database.cursor()
        
        if tafsir == 0:  # Almysr
            cursor.execute("SELECT content FROM items WHERE verse_key = ?", (aya_id,))
            result = cursor.fetchall()
        
        database.close()
        return result if result else {"message": "No data found"}

    except Exception as e:
        return {"error": str(e)}


# Get audio for shi5
@app.get("/quran/audio/{shui5}/{surah}:{aya_id}")
def audio(shui5, surah, aya_id):
    file_path = f"audio/quran/{shui5}/{surah}/{aya_id}.mp3"
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/mp3")
    else:
        return {"error": "File not found"}
