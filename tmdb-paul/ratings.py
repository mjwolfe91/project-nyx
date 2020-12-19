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

def generate_ratings_financials(volume)->pd.DataFrame:
    '''
    requires an api key.
    '''
    gross_margin=[]
    average_vote=[]
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

            average_vote.append(movie.vote_average)
            gross_margin.append(movie.revenue - movie.budget)
            movie_id.append(i)
            try:
                gross_margin_rate.append(movie.revenue/(movie.revenue + movie.budget))
            except:
                gross_margin_rate.append(0)
        except:
            pass

    average_vote = pd.Series(average_vote)
    gross_margin_rate = pd.Series(gross_margin_rate)
    gross_margin = pd.Series(gross_margin)
    movie_id = pd.Series(movie_id)

    rating_financials = pd.concat([movie_id, average_vote, gross_margin, round(gross_margin_rate, 2)], axis=1)
    rating_financials.columns = ['movie_id','average_rating','gross_margin','gross_margin_pct']
    
    return rating_financials

rating_financials_report = generate_ratings_financials(volume=10000) # 10000 movies x 1 rating each = 10k samples

tbl_rating_financials = """SELECT average_rating, sum(gross_margin) as ratings_gross_margin, avg(gross_margin_pct) as ratings_gross_margin_pct
                           FROM rating_financials_report
                           group by average_rating
                           order by ratings_gross_margin_pct desc, ratings_gross_margin desc
                        """
final_table_ratings = ps.sqldf(tbl_rating_financials, locals())
final_table_ratings.to_sql(name='ratings',
                        con=conn,
                        if_exists='replace',
                        index=False,
                        flavor='mysql')
