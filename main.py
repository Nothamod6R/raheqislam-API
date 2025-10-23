import _sqlite3
import json
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



"""
    Raheq islam API Version 1

    Developers:
       - Pixly
"""



# ====================================================================
# Quran API
# ====================================================================

# Get chapters
@app.get("/api/v1/quran/chapters")
def get_chapters():
    f = open("database/surah.json", encoding='utf-8')
    data = json.load(f)
    f.close()
    return data

# Get aya by id
@app.get("/api/v1/quran/ayas/{aya_id}")
def get_aya(aya_id: str):
    database = _sqlite3.connect("database/quran.db", check_same_thread=False)
    cursor = database.cursor()
    cursor.execute("SELECT * FROM verses WHERE verse_key = ?", (aya_id,))
    rows = cursor.fetchall()
    result = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
    database.close()
    return {"verses": result}


# Get ayas by page
@app.get("/api/v1/quran/ayas/pages/{page}")
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
@app.get("/api/v1/quran/tafsir/{tafsir}/{aya_id}")
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
#/api/v1/quran/audio/{shui5}/{surah}:{aya_id}
@app.get("/api/v1/quran/audio/{shui5}/{surah_aya}")
def audio(shui5, surah_aya):
    surah = surah_aya[:surah_aya.index(":")]
    aya_id = surah_aya[surah_aya.index(":")+1:]
    file_path = f"audio/quran/{shui5}/{surah}/{aya_id}.mp3"
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="audio/mp3")
    else:
        return {"error": "File not found"}
    
# Get shi5
@app.get("/quran/rections")
def rections():
    f = open("shi5.json", encoding='utf-8')
    data = json.load(f)
    f.close()
    return data

# ====================================================================
# Athker
# ====================================================================

@app.get("/api/v1/athker/all")
def get_main_info_thker():
    f = open("database/athkar.json", encoding="utf-8")
    data = json.load(f)
    f.close()
    return data

# ====================================================================
# Questions
# ====================================================================

@app.get("/api/v1/questions/show")
def show_questions():
    f = open("database/questions.json", encoding='utf-8')
    data = json.load(f)
    f.close()
    return data

@app.get("/api/v1/questions/random")
def questions_random():
    try:
        with open("database/questions.json", encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return {"error": "ERROR 404: Not Find database/questions.json"}
    except json.JSONDecodeError:
        return {"error": "ERROR: questions.json file JSONCODE is wrong."}

    if not isinstance(data, list) or not data:
        return {"error": "Empty question"}

    random_question_object = random.choice(data)

    return random_question_object
