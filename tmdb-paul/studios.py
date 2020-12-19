import math
import numpy as np
import pandas as pd
import pandasql as ps
import tmdbsimple as tmdb
tmdb.API_KEY = '40489ab6ba001d13b45d8b38709f687c'

def generate_studio_financials(volume):
    '''
    requires an api key.
    '''
    gross_margin=[]
    production_studios=[]
    gross_margin_rate=[]
    movie_id=[]

    if volume < 12:
        volume = 12
    else:
        volume = math.floor(volume)

    for i in range(11, volume):
        try:
            movie = tmdb.Movies(i) # there are 25,777 starting at id 11
            movie.info()

            for studio in movie.production_companies:
                production_studios.append(studio['name'])
                gross_margin.append(movie.revenue - movie.budget)
                movie_id.append(i)
                try:
                    gross_margin_rate.append(movie.revenue/(movie.revenue + movie.budget))
                except:
                    gross_margin_rate.append(0)
        except:
            pass

    production_studios = pd.Series(production_studios)
    gross_margin_rate = pd.Series(gross_margin_rate)
    gross_margin = pd.Series(gross_margin)
    movie_id = pd.Series(movie_id)

    studio_financials = pd.concat([movie_id, production_studios, gross_margin, round(gross_margin_rate, 2)], axis=1)
    studio_financials.columns = ['movie_id','production_studio','gross_margin','gross_margin_pct']
    
    return studio_financials

studio_financial_report = generate_studio_financials(volume=3333) # 3333 movies X 3 production studios each = ~10k samples

tbl_studio_financials = """SELECT production_studio, sum(gross_margin) as studio_gross_margin, avg(gross_margin_pct) as studio_gross_margin_pct
                          FROM studio_financial_report
                          group by production_studio
                          order by studio_gross_margin_pct desc, studio_gross_margin desc
                       """

final_table_studios = ps.sqldf(tbl_studio_financials, locals())
final_table_studios
