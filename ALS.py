
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

from pyspark.sql.functions import col, explode
from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql import SQLContext
from pyspark.ml.evaluation import RegressionEvaluator
from pyspark.ml.recommendation import ALS
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator
import pickle

sc = SparkContext
sqlContext = SQLContext(sc)

# sc.setCheckpointDir('checkpoint')
spark = SparkSession.builder.appName('Recommendations').getOrCreate()

movies = sqlContext.read.format('jdbc').options(url='jdbc:mysql://172.116.176.142:3306',
                                            user='root',
                                            password='projectnyx1234',
                                            dbtable='movielens.movies_raw').load()

ratings = sqlContext.read.format('jdbc').options(url='jdbc:mysql://172.116.176.142:3306',
                                            user='root',
                                            password='projectnyx1234',
                                            dbtable='movielens.ratings_raw').load()

ratings = ratings.\
    withColumn('userId', col('userId').cast('integer')).\
    withColumn('movieId', col('movieId').cast('integer')).\
    withColumn('rating', col('rating').cast('float')).\
    drop('timestamp')

numerator = ratings.select("rating").count()

# Count the total number of ratings in the dataset
numerator = ratings.select("rating").count()

# Count the number of distinct userIds and distinct movieIds
num_users = ratings.select("userId").distinct().count()
num_movies = ratings.select("movieId").distinct().count()

# Set the denominator equal to the number of users multiplied by the number of movies
denominator = num_users * num_movies

# Divide the numerator by the denominator
sparsity = (1.0 - (numerator *1.0)/denominator)*100

# Group data by userId, count ratings
userId_ratings = ratings.groupBy("userId").count().orderBy('count', ascending=False)

# Group data by movieId, count ratings
movieId_ratings = ratings.groupBy("movieId").count().orderBy('count', ascending=False)

# Create test and train set
(train, test) = ratings.randomSplit([0.8, 0.2], seed = 1234)

# Create ALS model
als = ALS(userCol="userId", itemCol="movieId", ratingCol="rating", nonnegative = True, implicitPrefs = False, coldStartStrategy="drop")

# Add hyperparameters and their respective values to param_grid
param_grid = ParamGridBuilder() \
            .addGrid(als.rank, [10, 50, 100, 150]) \
            .addGrid(als.regParam, [.01, .05, .1, .15]) \
            .build()

# Define evaluator as RMSE and print length of evaluator
evaluator = RegressionEvaluator(metricName="rmse", labelCol="rating", predictionCol="prediction")

# Build cross validation using CrossValidator
cv = CrossValidator(estimator=als, estimatorParamMaps=param_grid, evaluator=evaluator, numFolds=5)

#Fit cross validator to the 'train' dataset
model = cv.fit(train)

#Extract best model from the cv model above
best_model = model.bestModel


# Predictions
test_predictions = best_model.transform(test)
RMSE = evaluator.evaluate(test_predictions)

# Generate n Recommendations for all users
nrecommendations = best_model.recommendForAllUsers(10)

nrecommendations = nrecommendations\
    .withColumn("rec_exp", explode("recommendations"))\
    .select('userId', col("rec_exp.movieId"), col("rec_exp.rating"))

with open("./recommendations.pkl", "wb") as model_pkl:
    pickle.dump(nrecommendations, model_pkl)
