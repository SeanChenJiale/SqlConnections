# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 11:11:00 2024

@author: ChenS11
"""
##requires the package, download via pip using 
##pip install mysql-connector-python
import logging
import time
import mysql.connector 
from pandas import DataFrame
# conn = mysql.connector.connect(user = 'root',
#                                host = 'localhost',
#                               database = 'seanutsii',
#                               password = '<inputpasswordhere>')
 
# Set up logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
# Log to console
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger.addHandler(handler)
# Also log to a file
file_handler = logging.FileHandler("cpy-errors.log")
file_handler.setFormatter(formatter)
logger.addHandler(file_handler) 
def connect_to_mysql(config, attempts=3, delay=2):
    attempt = 1
    # Implement a reconnection routine
    while attempt < attempts + 1:
        try:
            return mysql.connector.connect(**config)
        except (mysql.connector.Error, IOError) as err:
            if (attempts is attempt):
                # Attempts to reconnect failed; returning None
                logger.info("Failed to connect, exiting without a connection: %s", err)
                return None
            logger.info(
                "Connection failed: %s. Retrying (%d/%d)...",
                err,
                attempt,
                attempts-1,
            )
            # progressive reconnect delay
            time.sleep(delay ** attempt)
            attempt += 1
    return None 
config = {
  'user': 'root',
  'password': '<inputpasswordhere>',
  'host': 'localhost',
  'database': 'seanutsii',
  'raise_on_warnings': True
}


cnx = connect_to_mysql(config, attempts=3)
if cnx and cnx.is_connected():
    with cnx.cursor() as cursor:
        cursor.execute("SELECT * FROM common_values_str ")
        column_Names  = cursor.description
        result = [{column_Names[index][0]: column for index, column in enumerate(value)} for value in cursor.fetchall()]
        df = DataFrame(result)
df.columns
len(df)

# Disconnecting from the server
# conn.close()