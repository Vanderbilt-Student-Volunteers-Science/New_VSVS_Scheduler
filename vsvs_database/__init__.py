CLASS_TABLE_CREATION_SQL = '''
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

VOLUNTEER_TABLE_CREATION_SQL = '''
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

TEACHER_TABLE_CREATION_SQL = '''
    CREATE TABLE IF NOT EXISTS Teacher( 
        Email       VARCHAR(50) PRIMARY KEY CHECK (Email LIKE '%@%.%'),
        School      VARCHAR(50),  
        Phone       CHAR(10), 
        First_name  VARCHAR(50) NOT NULL, 
        Last_name   VARCHAR(50) NOT NULL);
    '''

LESSONS_TABLE_CREATION_SQL = '''
    CREATE TABLE IF NOT EXISTS Lesson( 
        Name        VARCHAR(50) PRIMARY KEY, 
        Num_of_kits INT         NOT NULL    DEFAULT(0), 
        Grade       INT );
    '''