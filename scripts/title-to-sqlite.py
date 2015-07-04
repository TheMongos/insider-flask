import json
import sqlite3
# import requests

titles_file = 'tmdb_movies.txt'
label = 'Movie'
con = sqlite3.connect('test_db')
id = 0
cur = con.cursor()
cur.execute("CREATE TABLE Title (title TEXT, item_id INT, poster_path TEXT, year INT)")

def get_new_id():
    id += 1
    return id

with open (titles_file, 'r') as f_in:
    counter = 0
    more_than_one = 0
    no_genre_counter = 0
    for line in f_in:
        obj = json.loads(line)

        cur.execute("INSERT INTO Title ({0}, {1}, {2}, {3})".format(obj['title'], get_new_id(), obj['poster_path'], obj['release_date'].split('-')[0]))

        counter = counter + 1
        # for debug
        #if counter == 100:
           # break

print counter