import json
import ast
import sqlite3
# import requests

titles_file = '/home/recomate/tmdb/tmdb_movies.txt'
con = sqlite3.connect('../db/search_title.db.new')
id = 1
cur = con.cursor()

with con:
	with open (titles_file, 'r') as f_in:
	    more_than_one = 0
	    for line in f_in:
		try:
			obj = json.loads(line)
		except Exception as e:
			obj = ast.literal_eval(line)

		cur.execute("UPDATE Title SET popularity = ? WHERE title = ? AND item_id = ?", (obj['popularity'], obj['title'], id))
		id += 1

cur.close()
con.close()
