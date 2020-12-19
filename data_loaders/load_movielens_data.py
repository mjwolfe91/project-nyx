from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from pyspark import SparkFiles
import zipfile
import findspark

findspark.add_packages('mysql:mysql-connector-java:8.0.11')

conf = SparkConf().setAppName("load_movielens_base_data").setMaster("local")
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)

sc.addFile("http://files.grouplens.org/datasets/movielens/ml-25m.zip")

movie_lens_files = ["genome-scores","genome-tags","links",
                     "movies","ratings","tags"]

def load_csv_data(zipFile, files):

    with zipfile.ZipFile(zipFile) as zip:
        for file in files:
            extracted = zip.extract("ml-25m/{}.csv".format(file))
            df = sqlContext.read.csv(extracted, header=True)
            df.write.format("jdbc").options(
                url="jdbc:mysql://172.116.176.142:3306/data",
                driver='com.mysql.jdbc.Driver',
                dbtable=f'{file}_raw'.replace("-","_"),
                user='root',
                password='projectnyx1234').mode('overwrite').save()

if __name__ == '__main__':
    load_csv_data(SparkFiles.get("ml-25m.zip"), movie_lens_files)
