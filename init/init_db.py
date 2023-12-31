import sqlite3
from pathlib import Path

# get the path to the data directory
data_dir = Path(__file__).parents[1].joinpath('data')

connection = sqlite3.connect(data_dir.joinpath('database.db'))

with open(data_dir.joinpath('schema.sql')) as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('First Post', 'Content for the first post')
            )

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Second Post', 'Content for the second post')
            )

connection.commit()
connection.close()
