# -*- coding: utf-8 -*-

import psycopg2
from sqlalchemy import create_engine
import pandas as pd

class SQL_functions:
    def __init__(self, dbname = 'caponechallenge', username='postgres', password='password', host='localhost'):
        self.dbname = dbname
        self.username = username
        self.password = password
        self.db_conn = f'postgresql+psycopg2://{username}:{password}@{host}/{dbname}'
    
    def sql_connection(self):
        '''
        Connect to PostgreSQL via psycopg2
        '''
        conn = psycopg2.connect(f'dbname={self.dbname} user={self.username} password={self.password}')
        return conn
    
    def sql_alchemy_engine(self, echo=False):
        '''
        Create a sql_alchemy engine to import pandas dataframes into SQL database. I am using this instead of psycopg2 
        in order to save time versus using psycopg2 and CREATE TABLE or INSERT syntax.
        '''
        engine = create_engine(f'{self.db_conn}', echo=echo)
        return engine
    
    def run_sql_query(self, query, engine):
        '''
        Read SQL queries into pandas dataframe.
        '''
        df = pd.read_sql_query(query, engine)
        return df
    
    def update_NULL_allColumns(self, column_list, table_name, schema_name, conn):
        '''
        Uses the update_Null_values function to loop over a provided column_list and update NULL values from pandas into 
        NULL values recognized by SQL. 
        '''
        for column in column_list:
            self.update_NULL_values(table_name, schema_name, column, conn = conn)    
            
    def update_NULL_values(self, table_name, table_schema, column_name, conn, to_replace= 'None'):
        '''
        Manage NULL datatypes in SQL after conversion from pandas into SQL. This function updates the string None to NULL. 
        '''
        sql_update = f'''
            UPDATE {table_name}
            SET {column_name} = NULL
            WHERE {column_name} = to_replace
            '''
        try:
            db_cursor = conn.cursor()
            db_cursor.execute(sql_update)
            conn.commit()
            print(f'{column_name} updated successfully.')
        except:
            conn.rollback()
            print(f'{column_name} failed to update')
        db_cursor.close()    
        
    def create_view(self, view_name, sql_query, conn):
        '''
        Create a view in PostgreSQL. In this project, I created views for some of my SQL queries. 
        Views are more efficient for repeated queries. 
        '''
        view = f'''CREATE OR REPLACE VIEW {view_name} AS 
                  ({sql_query})
      
                  '''
        try:
            db_cursor = conn.cursor()
            db_cursor.execute(view)
            conn.commit()
        except:
            conn.rollback()
            raise
        db_cursor.close()    
        print('View created successfully') 
        
    def create_table(self, table_name, columns, conn):
        '''
        I used SQLAlchemy engine with pd.to_sql to create the tables the lazy way. But, to show I can also create tables 
        using SQL syntax, it would look something like this.
        '''
        table = f'''CREATE TABLE {table_name} ({columns}) 
                  '''
        try:
            db_cursor = conn.cursor()
            db_cursor.execute(table)
            conn.commit()
        except:
            conn.rollback()
            raise
        db_cursor.close()    
        print('Table created successfully')
    
    def insert_into_table(self, table_name, columns, values, conn):
        '''
        Again, I chose a method that avoided me having to use INSERT statements to save time. However, if I were to use 
        SQL syntax, it would look something like this. 
        '''
        insert = f''' INSERT INTO {table_name} ({columns})
                        VALUES ({values})
                '''
        try: 
            db_cursor= conn.cursor()
            db_cursor.execute(insert)
            conn.commit()
        except:
            conn.rollback()
            raise
        db_cursor.close()
        print('Insert executed successfully.')