import sys
import mysql.connector
from db_config import config

try:
     mycon=mysql.connector.connect(**config)
except mysql.connector.Error as err:
    print(f"Error connecting to database: {err}")
    sys.exit()

mycursor=mycon.cursor()
user_id=None
admin_id=None

