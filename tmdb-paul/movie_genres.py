import math
import numpy as np
import pandas as pd
import pandasql as ps
import tmdbsimple as tmdb
import pymysql

tmdb.API_KEY = '40489ab6ba001d13b45d8b38709f687c'

conn = pymysql.connect(host="172.116.176.142:3306", port=3306, user='root', passwd='projectnyx1234')
conn.cursor().execute("CREATE DATABASE IF NOT EXISTS tmdb")
conn = pymysql.connect(host="172.116.176.142:3306",
                       port=3306,
                       user='root',
                       passwd='projectnyx1234',
                       db='tmdb')

def generate_genre_financials(volume)->pd.DataFrame:
    '''
    requires an api key.
    inputs:
        all: generates all 25,788 movies available
        some: generates a random sample of 1000 movies
        sample: generates a random sample of 100 movies
    '''
    gross_margin=[]
    genre_types=[]
    gross_margin_rate=[]
    movie_id=[]

    if volume < 12:
        volume = 12
    else:
        volume = volume

    for i in range(11, math.floor(volume)):
        try:
            movie = tmdb.Movies(i) # there are 25,777 starting at id 11
            movie.info()

            for genre in movie.genres:
                genre_types.append(genre['name'])
                gross_margin.append(movie.revenue - movie.budget)
                movie_id.append(i)
                try:
                    gross_margin_rate.append(movie.revenue/(movie.revenue + movie.budget))
                except:
                    gross_margin_rate.append(0)
        except:
            pass

    genre_types = pd.Series(genre_types)
    gross_margin_rate = pd.Series(gross_margin_rate)
    gross_margin = pd.Series(gross_margin)
    movie_id = pd.Series(movie_id)

    genre_financial = pd.concat([movie_id, genre_types, gross_margin, round(gross_margin_rate, 2)], axis=1)
    genre_financial.columns = ['movie_id','genre_type','gross_margin','gross_margin_pct']
    
    return genre_financial

genre_financials_report = generate_genre_financials(volume=5000) # 5000 movies x 1 or 2 genres each = ~10k samples?

tbl_genre_financials = """SELECT genre_type, sum(gross_margin) as genre_gross_margin, avg(gross_margin_pct) as genre_gross_margin_pct
                          FROM genre_financials_report
                          group by genre_type
                          order by genre_gross_margin_pct desc, genre_gross_margin desc
                       """
final_table_genres = ps.sqldf(tbl_genre_financials, locals())
final_table_genres.to_sql(name='genres',
                        con=conn,
                        if_exists='replace',
                        index=False,
                        flavor='mysql')
