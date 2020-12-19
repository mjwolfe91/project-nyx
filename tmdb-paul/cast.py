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

def generate_cast_financials(volume)->pd.DataFrame:
    '''
    requires an api key.
    '''
    gross_margin=[]
    cast=[]
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

            for i in range(0,10):# get the first 10 cast members listed #for i in range(0,len(movie.credits())):
                cast.append(movie.credits()['cast'][i]['name'])
                gross_margin.append(movie.revenue - movie.budget)
                movie_id.append(i)
                try:
                    gross_margin_rate.append(movie.revenue/(movie.revenue + movie.budget))
                except:
                    gross_margin_rate.append(0)
        except:
            pass

    cast = pd.Series(cast)
    gross_margin_rate = pd.Series(gross_margin_rate)
    gross_margin = pd.Series(gross_margin)
    movie_id = pd.Series(movie_id)

    cast_financials = pd.concat([movie_id, cast, gross_margin, round(gross_margin_rate, 2)], axis=1)
    cast_financials.columns = ['movie_id','cast_member','gross_margin','gross_margin_pct']
    
    return cast_financials

cast_financials_report = generate_cast_financials(volume=1000) # 1000 movies x 10 cast members each = 10k samples

tbl_cast_financials = """SELECT cast_member, avg(gross_margin_pct) as cast_gross_margin_pct, sum(gross_margin) as cast_gross_margin, count(*) as cast_count
                         FROM cast_financials_report
                         group by cast_member
                         order by cast_gross_margin_pct desc, cast_gross_margin desc, cast_count desc
                      """
final_table_cast = ps.sqldf(tbl_cast_financials, locals())
final_table_cast.to_sql(name='cast',
                        con=conn,
                        if_exists='replace',
                        index=False,
                        flavor='mysql')
