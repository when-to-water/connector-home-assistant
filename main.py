import os
import sqlalchemy
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

strEngine = f"mariadb+mariadbconnector://{os.getenv('MARIADB_USER')}:{os.getenv('MARIADB_KEY')}@{os.getenv('MARIADB_HOST')}:{os.getenv('MARIADB_PORT')}/{os.getenv('MARIADB_DATABASE')}"

engine = sqlalchemy.create_engine(strEngine)

df = pd.read_sql(
    "SELECT state_id,entity_id,state,attributes, \
last_changed,last_updated,created,old_state_id \
FROM states \
WHERE entity_id LIKE '%efekta%'and state <>'unavailable' \
ORDER BY `states`.`created`  DESC",
    engine,
)

# Results
print(df.head(5))
