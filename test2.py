import _sqlite3

db = _sqlite3.connect("database/quran.db")
cursor = db.cursor()

cursor.execute(""" 
CREATE TABLE "verse" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT,
    "number" SMALLINT NOT NULL CHECK("number" >= 0),
    "content" VARCHAR(1024) NOT NULL,
    "chapter_id" BIGINT NOT NULL,
    "group_id" BIGINT,
    "page_id" BIGINT,
    "part_id" BIGINT,
    "quarter_id" BIGINT,
    "verse_key" TEXT,
    "qcf_data" TEXT
);
""")

db.commit()
db.close()
