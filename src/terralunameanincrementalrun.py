from pyspark.sql.functions import mean
from pyspark.sql import SparkSession
from pyspark.sql import Row
from pyspark.sql.functions import col
from pyspark.sql.functions import concat
from pyspark.sql.functions import isnan, when, count, col




spark = SparkSession.builder.master("local").appName("PySpark_Postgres_test").getOrCreate()
dburl="jdbc:postgresql://ec2-13-40-49-105.eu-west-2.compute.amazonaws.com:5432/testdb"


max = spark.sql("select max(coin_id) from pythongroup.terralunameanproject as max")

max = max.first()['max(coin_id)']

query="(select * from terralunameanproject where coin_id >"+str(max)+ ") as tb"
df = spark.read.format("jdbc").option("url",dburl) \
    .option("driver", "org.postgresql.Driver").option("dbtable", query) \
    .option("user", "consultants").option("password", "WelcomeItc@2022").load()


query="(select * from terralunameanproject where coin_id >"+str(max)+ ") as tb"
df = spark.read.format("jdbc").option("url",dburl) \
    .option("driver", "org.postgresql.Driver").option("dbtable", query) \
    .option("user", "consultants").option("password", "WelcomeItc@2022").load()

df.select([count(when(isnan(c) | col(c).isNull(), c)).alias(c) for c in ["price"]])
null_col = df.filter(col("price").isNull())
mean_val = df.select(mean(col("price"))).collect()[0][0]
df_mean = df.fillna(mean_val, subset=["price"])

df_mean.show()

df_mean.write.mode('append') \
    .saveAsTable("pythongroup.terralunameanproject")