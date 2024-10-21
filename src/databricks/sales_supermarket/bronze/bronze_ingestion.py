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

dbutils.widgets.text('schema_name', '')
dbutils.widgets.text('table_name', '')
dbutils.widgets.text('data_format', '')
dbutils.widgets.text('write_mode', '')

schema_name = dbutils.widgets.get('schema_name')
table_name = dbutils.widgets.get('table_name')
data_format = dbutils.widgets.get('data_format')
write_mode = dbutils.widgets.get('write_mode')

# COMMAND ----------

# MAGIC %md
# MAGIC ### Defining Variables

# COMMAND ----------

source_path =  f'/Volumes/raw/{schema_name}/sales_db/{table_name}'
checkpoint_path = f'/Volumes/raw/{schema_name}/sales_db/{table_name}_checkpoint'

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC ### Running ingest class

# COMMAND ----------

if not table_exists(spark, catalog, schema_name, table_name):
    print(f'Table {schema_name}.{table_name} does not exist, creating now...')

    dbutils.fs.rm(checkpoint_path, recurse=True)
    
    bronze_ingestion = Ingestor(spark          =   spark,
                                catalog        =   catalog,
                                schema_name    =   schema_name,
                                table_name     =   table_name,
                                data_format    =   data_format,
                                write_mode     =   write_mode)
    bronze_ingestion.execute_load(source_path)
    print('> Table created successfully')
else:
    print('> Table already exists')
