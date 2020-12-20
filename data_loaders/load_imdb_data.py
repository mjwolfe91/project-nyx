from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from pyspark import SparkFiles

import findspark

findspark.add_packages('mysql:mysql-connector-java:8.0.11')

conf = SparkConf().setAppName("load_imdb_base_data").setMaster("local")
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)

imdb_files = ["name.basics", "title.akas", "title.basics", "title.crew", "title.episode", "title.principals", "title.ratings"]

def load_tsv_data(tsv_files):
    for file in tsv_files:
        sc.addFile(f"https://datasets.imdbws.com/{file}.tsv.gz")
        out_df = sqlContext.read.csv(SparkFiles.get(f"{file}.tsv.gz"), sep=r'\t', header=True)
        out_df.repartition(10).write.format("jdbc").options(
            url="jdbc:mysql://172.116.176.142:3306/data",
            driver='com.mysql.cj.jdbc.Driver',
            dbtable=f'data.imdb_{file}_raw'.replace(".", "_"),
            user='root',
            password='projectnyx1234',
            batchsize=100000,
            useSSL=False).mode('overwrite').save()

if __name__ == '__main__':
    load_tsv_data(imdb_files)
