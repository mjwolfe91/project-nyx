from pyspark import SparkContext, SparkConf
from pyspark.sql import SQLContext
from pyspark import SparkFiles

import findspark

findspark.add_packages('mysql:mysql-connector-java:8.0.11')

conf = SparkConf().setAppName("load_movielens_base_data").setMaster("local")
sc = SparkContext(conf=conf)
sqlContext = SQLContext(sc)

sc.addFile("https://s3.amazonaws.com/amazon-reviews-pds/tsv/amazon_reviews_us_Video_DVD_v1_00.tsv.gz")

def load_tsv_data(tsv_file, output_name):
    out_df = sqlContext.read.csv(SparkFiles.get(tsv_file), sep=r'\t', header=True)
    out_df.write.format("jdbc").options(
        url="jdbc:mysql://172.116.176.142:3306/data",
        driver='com.mysql.jdbc.Driver',
        dbtable=f'{output_name}_raw'.replace("-", "_"),
        user='root',
        password='projectnyx1234',
        batchsize=100000).mode('overwrite').save()

if __name__ == '__main__':
    load_tsv_data("amazon_reviews_us_Video_DVD_v1_00.tsv.gz", "amazon_video_reviews")
