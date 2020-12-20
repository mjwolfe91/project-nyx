
'''
__author__ = "David Stroud"
__project__ = "NYX"
__date__ = "12/19/2020"
__credits__ = [Shehal Nair ~ https://towardsdatascience.com/
                build-recommendation-system-with-pyspark-using-alternating-
                least-squares-als-matrix-factorisation-ebe1ad2e7679]
__version__ = "1.0.0"
__email__ = "jdstroud@troy.edu"
'''
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark import SQLContext
from pyspark.ml.recommendation import ALS, ALSModel
import uvicorn
import findspark
import time

time.sleep(4)

findspark.add_packages('mysql:mysql-connector-java:8.0.11')


sc = SparkContext()
sqlContext = SQLContext(sc)

# sc.setCheckpointDir('checkpoint')
spark = SparkSession.builder.appName('Recommendations').getOrCreate()

movies = sqlContext.read.format('jdbc').options(url='jdbc:mysql://mysql:3306/movielens?allowPublicKeyRetrieval=true',
                                            user='root',
                                            driver='com.mysql.cj.jdbc.Driver',
                                            password='projectnyx1234',
                                            dbtable='movies_raw',
                                            useSSL=False,
                                            fetchsize=100000).load()

ratings = sqlContext.read.format('jdbc').options(url='jdbc:mysql://mysql:3306/movielens?allowPublicKeyRetrieval=true',
                                            driver='com.mysql.cj.jdbc.Driver',
                                            user='root',
                                            password='projectnyx1234',
                                            dbtable='ratings_raw',
                                            useSSL=False,
                                            fetchsize=100000).load()

app = FastAPI(title="Customer Recommendations", version="1.0.0", root_path="/stroud_api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Let's load in the model we used before
rec = ALSModel.load("/app/finalized_model.sav")

class Recommendation(BaseModel):
    """
    todo: get this info from Stroud!!
    """
    userId: int
    movieId: int
    rating: float

@app.post("/predict")
def predict(sample: Recommendation):
    """
    Unpack the responses, predict on the input variables, and return the prediction.
    """
    responses = [
        [sample.userId, sample.movieId, sample.rating]
    ]

    return rec.predict(inputs)[0]

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, debug=False)
