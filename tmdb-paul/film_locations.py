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


def generate_location_financials(volume)->pd.DataFrame:
    '''
    requires an api key.
    '''
    gross_margin=[]
    production_countries=[]
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

            for country in movie.production_countries:
                production_countries.append(country['name'])
                gross_margin.append(movie.revenue - movie.budget)
                movie_id.append(i)
                try:
                    gross_margin_rate.append(movie.revenue/(movie.revenue + movie.budget))
                except:
                    gross_margin_rate.append(0)
        except:
            pass

    production_countries = pd.Series(production_countries)
    gross_margin_rate = pd.Series(gross_margin_rate)
    gross_margin = pd.Series(gross_margin)
    movie_id = pd.Series(movie_id)

    location_financials = pd.concat([movie_id, production_countries, gross_margin, round(gross_margin_rate, 2)], axis=1)
    location_financials.columns = ['movie_id','production_country','gross_margin','gross_margin_pct']
    
    return location_financials

location_financials_report = generate_location_financials(volume=5000) # 5000 movies x 1-2 locations each = ~10k samples

tbl_location_financials = """SELECT production_country, sum(gross_margin) as location_gross_margin, avg(gross_margin_pct) as location_gross_margin_pct
                          FROM location_financials_report
                          group by production_country
                          order by location_gross_margin_pct desc, location_gross_margin desc
                       """
final_table_locations = ps.sqldf(tbl_location_financials, locals())
final_table_locations.to_sql(name='locations',
                        con=conn,
                        if_exists='replace',
                        index=False,
                        flavor='mysql')
