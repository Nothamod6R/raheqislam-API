import _sqlite3
import json
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import random


# Setup API

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
       - Owais19


    © Copyright 2025 Raheq alislam
"""


# ==========================================================
# Raheq islam API Version 1
# ==========================================================

# //////////////////////////
# Quran
# //////////////////////////

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
    cursor.execute("SELECT * FROM verse WHERE verse_key = ?", (aya_id,))
    rows = cursor.fetchall()
    result = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
    database.close()
    return {"verses": result}


# Get ayas by page
@app.get("/api/v1/quran/ayas/pages/{page}")
def get_aya_page(page):
    database = _sqlite3.connect("database/quran.db", check_same_thread=False)
    database.row_factory = _sqlite3.Row
    cursor = database.cursor()

    cursor.execute("SELECT * FROM verse WHERE page_id = ?", (page,))
    rows = cursor.fetchall()

    result = [dict(row) for row in rows]
    database.close()

    return {"verses":result}

# Get ayas by surah
@app.get("/api/v1/quran/ayas/surah/{surah_id}")
def get_aya_surah(surah_id):
    database = _sqlite3.connect("database/quran.db", check_same_thread=False)
    database.row_factory = _sqlite3.Row
    cursor = database.cursor()

    cursor.execute("SELECT * FROM verse WHERE chapter_id = ?", (surah_id,))
    rows = cursor.fetchall()

    result = [dict(row) for row in rows]
    database.close()

    return {"verses":result}
    

# Get tafsir by aya
@app.get("/api/v1/quran/tafsir/{tafsir}/{aya_id}")
def get_tafsir(tafsir, aya_id):
    try:
        database = _sqlite3.connect("database/tafsir.db", check_same_thread=False)
        cursor = database.cursor()
        
        if tafsir == "0":  # Almysr
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

# //////////////////////////
# Hadith
# //////////////////////////

BOOKS = {
    0: "malkis_muwatta",
    1: "musnad_ahmad_ibn_hanbal",
    2: "sahih_al_bukhari",
    3: "sahih_muslim",
    4: "sunan_abu_dawud",
    5: "sunan_al_darimi",
    6: "sunan_al_nasai",
    7: "sunan_al_tirmidhi",
    8: "sunan_ibn_maja"
}

@app.get("/api/v1/hadith/{book_id}/{start_id}/{count_range}")
def get_hadith(book_id: int, start_id: int, count_range: int):


    if book_id not in BOOKS:
        return {"error": "book_id Unknow"}

    table = BOOKS[book_id]

    try:
        database = _sqlite3.connect("database/hadith.db", check_same_thread=False)
        cursor = database.cursor()

        end_id = start_id + count_range

        cursor.execute(
            f"SELECT * FROM {table} WHERE id BETWEEN ? AND ?",
            (start_id, end_id)
        )

        results = cursor.fetchall()

        return [{"id": r[0], "context": r[1]} for r in results]

    except Exception as e:
        return {"error": str(e)}


# example

@app.get("/api/v1/hadith/search")
def search_hadith(
    query: str,                 
    books: str = "all",         
    limit: int = 20,            
    offset: int = 0           
):
    
    try:
        db = _sqlite3.connect("database/hadith.db", check_same_thread=False)
        cursor = db.cursor()

        if books == "all":
            selected_tables = BOOKS.values()  
        else:
            ids = [int(b.strip()) for b in books.split(",")]
            selected_tables = [BOOKS[i] for i in ids if i in BOOKS]

        results = []

        for table in selected_tables:
            cursor.execute(
                f"""
                SELECT id, context, '{table}' as source
                FROM {table}
                WHERE context LIKE ?
                LIMIT ? OFFSET ?
                """,
                (f"%{query}%", limit, offset)
            )

            rows = cursor.fetchall()
            for r in rows:
                results.append({
                    "id": r[0],
                    "context": r[1],
                    "source": table
                })

        return {
            "count": len(results),
            "results": results
        }

    except Exception as e:
        return {"error": str(e)}

# //////////////////////////
# Athker
# //////////////////////////

# Get All athker
@app.get("/api/v1/athker/all")
def get_main_info_thker():
    f = open("database/athkar.json", encoding="utf-8")
    data = json.load(f)
    f.close()
    return data

# //////////////////////////
# Questions
# //////////////////////////

# Get all questions in questions.json
@app.get("/api/v1/questions/show")
def show_questions():
    f = open("database/questions.json", encoding='utf-8')
    data = json.load(f)
    f.close()
    return data

# Get random questions
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

# Get random questions by level
@app.get("/api/v1/questions/level/{level}")
def get_question_by_level(level):
    try:
        with open("database/questions.json", encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        return {"error": "ERROR 404: Not Find database/questions.json"}
    except json.JSONDecodeError:
        return {"error": "ERROR: questions.json file JSONCODE is wrong."}

    if not isinstance(data, list) or not data:
        return {"error": "Empty question"}

    filtered_questions = [q for q in data if str(q.get("level")) == str(level)]

    if not filtered_questions:
        return {"error": f"No questions found for level '{level}'"}

    random_question_object = random.choice(filtered_questions)

    return random_question_object