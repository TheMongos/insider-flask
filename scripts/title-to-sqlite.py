import json
import ast
import sqlite3
# import requests

titles_file = '/home/recomate/tmdb/tmdb_movies.txt'
label = 'Movie'
con = sqlite3.connect('../db/search_title.db')
id = 1
cur = con.cursor()
cur.execute("CREATE TABLE Title (title TEXT, item_id INT, poster_path TEXT, year INT)")
cur.execute("CREATE INDEX title_index ON Title (title)")

with con:
	with open (titles_file, 'r') as f_in:
	    counter = 0
	    more_than_one = 0
	    no_genre_counter = 0
	    for line in f_in:
		try:
			obj = json.loads(line)
		except Exception as e:
			obj = ast.literal_eval(line)

		cur.execute("INSERT INTO Title VALUES(?, ?, ?, ?)", (obj['title'], id, obj['poster_path'], obj['release_date'].split('-')[0]))
		id += 1

		counter = counter + 1
		# for debug
		#if counter == 100:
		   # break
cur.close()
con.close()
print counter
