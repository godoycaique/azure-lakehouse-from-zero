-- Databricks notebook source
CREATE EXTERNAL LOCATION raw URL 'abfss://raw@adlsdataplatformdev.dfs.core.windows.net/unitycatalog'
WITH (STORAGE CREDENTIAL ac-databricks-global)
COMMENT 'Raw Container'

-- COMMAND ----------

CREATE EXTERNAL LOCATION bronze URL 'abfss://bronze@adlsdataplatformdev.dfs.core.windows.net/unitycatalog'
WITH (STORAGE CREDENTIAL ac-databricks-global)
COMMENT 'Bronze Container'

-- COMMAND ----------

CREATE EXTERNAL LOCATION silver URL 'abfss://silver@adlsdataplatformdev.dfs.core.windows.net/unitycatalog'
WITH (STORAGE CREDENTIAL ac-databricks-global)
COMMENT 'Silver Container'

-- COMMAND ----------

CREATE EXTERNAL LOCATION gold URL 'abfss://gold@adlsdataplatformdev.dfs.core.windows.net/unitycatalog'
WITH (STORAGE CREDENTIAL ac-databricks-global)
COMMENT 'Gold Container'

-- COMMAND ----------



-- COMMAND ----------

CREATE CATALOG IF NOT EXISTS raw
MANAGED LOCATION 'abfss://raw@adlsdataplatformdev.dfs.core.windows.net/unitycatalog/'

-- COMMAND ----------

CREATE CATALOG IF NOT EXISTS bronze
MANAGED LOCATION 'abfss://bronze@adlsdataplatformdev.dfs.core.windows.net/unitycatalog/'

-- COMMAND ----------

CREATE CATALOG IF NOT EXISTS silver
MANAGED LOCATION 'abfss://silver@adlsdataplatformdev.dfs.core.windows.net/unitycatalog/'

-- COMMAND ----------

CREATE CATALOG IF NOT EXISTS gold
MANAGED LOCATION 'abfss://gold@adlsdataplatformdev.dfs.core.windows.net/unitycatalog/'
