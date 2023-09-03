import sqlite3

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

        self.create_classes_table ='''
            CREATE TABLE IF NOT EXISTS Classes( 
                Email       VARCHAR(50) NOT NULL,
                Start_time  CHAR(8)     NOT NULL, 
                End_time    CHAR(8)     NOT NULL, 
                Class_size  INT, 
                Grade       INT, 
                Group_num   INT         NOT NULL    DEFAULT(0),
                Weekday     VARCHAR(15) NOT NULL, 
                CHECK (Weekday IN ('Monday', 'Tuesday', 'Wednesday', 'Thursday')),
                FOREIGN KEY (Email) REFERENCES Teacher(Email),
                PRIMARY KEY (Email, Start_time, Weekday));
        '''

        self.create_volunteer_table = '''
            CREATE TABLE IF NOT EXISTS Volunteer ( 
                Email           VARCHAR(50)     PRIMARY KEY     CHECK (Email LIKE '%@%.%'), 
                First_name      VARCHAR(50)     NOT NULL, 
                Last_name       VARCHAR(50)     NOT NULL,
                Phone           CHAR(10)        UNIQUE          NOT NULL, 
                Leader          BOOLEAN         DEFAULT(FALSE),
                Monday          VARCHAR(100), 
                Tuesday         VARCHAR(100), 
                Wednesday       VARCHAR(100), 
                Thursday        VARCHAR(100), 
                Leader_interest BOOLEAN         DEFAULT (FALSE),
                TShirt          VARCHAR(3),
                College_yr      VARCHAR(20));
            ''' 
        
        self.create_teacher_table = '''
            CREATE TABLE IF NOT EXISTS Teacher( 
                Email       VARCHAR(50) PRIMARY KEY CHECK (Email LIKE '%@%.%'),
                School      VARCHAR(50),  
                Phone       CHAR(10), 
                First_name  VARCHAR(50) NOT NULL, 
                Last_name   VARCHAR(50) NOT NULL);
            '''
        
        self.create_lessons_table = '''
            CREATE TABLE IF NOT EXISTS Lesson( 
                Name        VARCHAR(50) PRIMARY KEY, 
                Num_of_kits INT         NOT NULL    DEFAULT(0), 
                Grade       INT );
            '''
        
        self.execute_query("creating volunteer table", self.create_volunteer_table)
        self.execute_query("creating teacher table", self.create_teacher_table)
        self.execute_query("creating classes table", self.create_classes_table)
        self.execute_query("creating lessons table", self.create_lessons_table)
    

        
        
        
        
        
        
        
        
        




