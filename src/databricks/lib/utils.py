# Databricks notebook source
def table_exists(spark, catalog, database, table):
    spark.sql(f'CREATE SCHEMA IF NOT EXISTS {catalog}.{schema_name}')
    count = (spark.sql(f"SHOW TABLES FROM {catalog}.{database}")
                  .filter(f"database = '{database}' AND tableName = '{table}'")
                  .count())
    return count == 1
