from pyspark.sql import SparkSession
# Basic Spark Dataframe Operations 


```jupyterpython
from pyspark.sql import SparkSession
```

```jupyterpython
spark = SparkSession.builder.appName("Basics").getOrCreate()
df = spark.read.json("/dataset/example.json")

# show table 
df.show()

df.printSchema()

df.columns

df.describe().show()
```

## Changing Schema Type

```jupyterpython
from pyspark.sql.types import (StructField, StringType, IntegerType, StructType)
data_scheme = [StructField("age", IntegerType(), True),
               StructField("name", StringType(), True)]

final_struc = StructType(fields=data_scheme)

df = spark.read.json('./datasets/example.json', schema=final_struc)

# query operation
df.select("age").show()

df.select("age", "name").show()
df.head(2)


# show transformed column 

df.withColumn("double_age", df["age"]*2).show()
df.withColumnRenamed("age", "new_age_renamed").show()
df.createOrReplaceTempView("people")

results = spark.sql("SELECT age FROM people WHERE name = 'Lalaland'")
result.show()
```

## Data Filtering in Spark Dataframes

```jupyterpython
spark = SparkSession.builder.appName('ops').getOrCreate()

df = spark.read.csv('./datasets/apple-stock/appl_stock.csv', inferSchema=True, header=True)

df.filter("Close < 500").show()

result = df.filter(df['Low'] == 197.16).collect()

row = result[0]

row.asDict()

```



