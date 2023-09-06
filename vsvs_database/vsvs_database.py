import sqlite3
from vsvs_database import VOLUNTEER_TABLE_CREATION_SQL, TEACHER_TABLE_CREATION_SQL, CLASS_TABLE_CREATION_SQL, LESSONS_TABLE_CREATION_SQL

class vsvs_database:
    def __init__(self, db_file_path: str = 'data/VSVS.db'):

        try:
            self.conn = sqlite3.connect(db_file_path)
            self.cursor = self.conn.cursor()
            print("Database connection successful")
        except sqlite3.Error as err:
            print(f"Error: '{err}'")

        self.create_tables()

        self.conn.close()
       
    def execute_query(self, context: str, query: str):
        try:
            self.cursor.execute(query)
            print(f"\nQuery executed successfully\n")
        except sqlite3.Error as err:
            print(f"Error {context}: '{err}'")   
    
    def create_tables(self):
        self.execute_query("creating volunteer table", VOLUNTEER_TABLE_CREATION_SQL)
        self.execute_query("creating teacher table", TEACHER_TABLE_CREATION_SQL)
        self.execute_query("creating classes table", CLASS_TABLE_CREATION_SQL)
        self.execute_query("creating lessons table", LESSONS_TABLE_CREATION_SQL)
    

        