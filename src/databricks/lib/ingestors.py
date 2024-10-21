# Databricks notebook source
from pyspark.sql.functions import lit
from datetime import datetime
import delta
from delta import DeltaTable

# COMMAND ----------

class Ingestor:
  
    def __init__(self, spark, catalog, schema_name, table_name, data_format, write_mode):
        self.spark = spark
        self.catalog = catalog
        self.schema_name = schema_name
        self.table_name = table_name
        self.format = data_format
        self.mode = write_mode

    def set_schema(self):
        self.data_schema = utils.import_schema(self.table_name)
    
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
           .saveAsTable(f"{self.catalog}.{self.schema_name}.{self.table_name}"))
        return True
    
    def vacuum(self):
        deltaTable = DeltaTable.forName(self.spark, f'{self.catalog}.{self.schema_name}.{self.table_name}')
        deltaTable.vacuum(720)
        return True
    
    def execute_load(self, path):
        df = self.load(path)
        df = df.withColumn('load_date', lit(datetime.now()))
        self.save(df)
        return self.vacuum()
