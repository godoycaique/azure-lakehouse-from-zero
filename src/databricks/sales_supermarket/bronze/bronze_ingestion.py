# Databricks notebook source
# MAGIC %md
# MAGIC
# MAGIC ### Run Commons Libs

# COMMAND ----------

# MAGIC %run ../../lib/ingestors

# COMMAND ----------

# MAGIC %run ../../lib/utils

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### Defining input parameters

# COMMAND ----------

catalog = 'bronze'

dbutils.widgets.text('database_name', '')
dbutils.widgets.text('table_name', '')
dbutils.widgets.text('source_format', '')
dbutils.widgets.text('write_mode', '')

database_name = dbutils.widgets.get('database_name')
table_name = dbutils.widgets.get('table_name')
source_format = dbutils.widgets.get('source_format')
write_mode = dbutils.widgets.get('write_mode')

# COMMAND ----------

# MAGIC %md
# MAGIC ### Defining Variables

# COMMAND ----------

source_path =  f'/Volumes/raw/{database_name}/sales_db/{table_name}'
checkpoint_path = f'/Volumes/raw/{database_name}/sales_db/{table_name}_checkpoint'

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### Running ingest class

# COMMAND ----------

bronze_ingestion = Ingestor(spark          =   spark,
                            catalog        =   catalog,
                            database_name  =   database_name,
                            table_name     =   table_name,
                            source_format  =   source_format,
                            write_mode     =   write_mode)

# COMMAND ----------

if not table_exists(spark, catalog, database_name, table_name):
    print(f'Table {database_name}.{table_name} does not exist, creating now...')

    dbutils.fs.rm(checkpoint_path, recurse=True)
    bronze_ingestion.execute_load(source_path)
    print('> Table created successfully')
else:
    print('> Table already exists, updating...')
    bronze_ingestion.execute_load(source_path)
    print(f'> Table updated successfully with {write_mode} mode...')
