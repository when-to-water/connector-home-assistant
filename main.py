# Module imports
import sys
import os
import sqlalchemy
from sqlalchemy import create_engine
import pandas as pd

strEngine = "mariadb+mariadbconnector://" + os.environ.get('MARIADB_USER') + ":" + os.environ.get('MARIADB_KEY') + "@" + \
os.environ.get('MARIADB_HOST') + ":" + os.environ.get('MARIADB_PORT') + "/" + os.environ.get('MARIADB_DATABASE')

engine = sqlalchemy.create_engine(strEngine)

# SQL Statement
df = pd.read_sql("SELECT state_id,entity_id,state,attributes, \
last_changed,last_updated,created,old_state_id \
FROM states \
WHERE entity_id LIKE '%efekta%'and state <>'unavailable' \
ORDER BY `states`.`created`  DESC",engine)

#Results 
print(df.head(5))