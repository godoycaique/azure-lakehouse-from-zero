# Databricks notebook source
from pyspark.sql.functions import lit
from datetime import datetime
import delta
from delta import DeltaTable

# COMMAND ----------

class Ingestor:
  
    def __init__(self, spark, catalog, database_name, table_name, source_format, write_mode):
        self.spark = spark
        self.catalog = catalog
        self.database_name = database_name
        self.table_name = table_name
        self.format = source_format
        self.mode = write_mode
    
    def load(self, path):
        df = (self.spark
                  .read
                  .format(self.format)
                  .load(path))
        return df
    
    def save(self, df):
        (df.write
           .format("delta")
           .mode(self.mode)
           .saveAsTable(f"{self.catalog}.{self.database_name}.{self.table_name}"))
        return True
    
    def vacuum(self):
        deltaTable = DeltaTable.forName(self.spark, f'{self.catalog}.{self.database_name}.{self.table_name}')
        deltaTable.vacuum(720)
        return True
    
    def execute_load(self, path):
        df = self.load(path)
        df = df.withColumn('load_date', lit(datetime.now()))
        self.save(df)
        return self.vacuum()
