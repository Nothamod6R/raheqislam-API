import _sqlite3

def search(book_name, start_id, count_range):
    try:
        database = _sqlite3.connect("database/hadith.db", check_same_thread=False)
        cursor = database.cursor()
        print("Connect Done")
        end_id = start_id + count_range
        cursor.execute(
            f"SELECT * FROM {book_name} WHERE id BETWEEN ? AND ?",
            (start_id, end_id)
        )
        results = cursor.fetchall()
        return results
    except Exception as e:
        return "end"
    
print(search("sahih_al_bukhari", 10, 1))