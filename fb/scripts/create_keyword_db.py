import sqlite3
from countries.models import KeyWord
import os

DB_PATH = 'keywords.db'
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
con = sqlite3.connect(DB_PATH)
cursor = con.cursor()
cursor.execute("""
CREATE TABLE keyword (
id INTEGER PRIMARY KEY AUTOINCREMENT,
word TEXT,
language TEXT,
number_in_dict INTEGER
)
""")

keywords = KeyWord.objects.all()
for k in keywords:
    try:
        command = f'INSERT INTO keyword (id, word, number_in_dict, language) VALUES ({k.pk}, "{k.word}","{k.number_in_dict}","{k.language_id}" );'
        cursor.execute(
            command
        )
    except Exception as error:
        print(error)
con.commit()



# con = sqlite3.connect('keywords.db')
# cursor = con.cursor()
# res = cursor.execute("""
# SELECT COUNT(*) FROM keyword;
# """)
# print(res.fetchall())


