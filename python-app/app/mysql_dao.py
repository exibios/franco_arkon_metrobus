import pandas as pd
import numpy as np
import os
import uuid


from mysql_driver import MySQLDriver

class MySQLDAO(MySQLDriver):
    def create_table(self, table_name, data_frame):
        """
        Create a MySQL table based on a pandas DataFrame.

        :param table_name: Name of the table to create.
        :param data_frame: pandas DataFrame to base the table schema on.
        """
        cursor = self.get_cursor()
        try:
            # Generate a CREATE TABLE statement dynamically
            columns = []
            for column, dtype in zip(data_frame.columns, data_frame.dtypes):
                if pd.api.types.is_integer_dtype(dtype):
                    columns.append(f"{column} INT")
                elif pd.api.types.is_float_dtype(dtype):
                    columns.append(f"{column} FLOAT")
                elif pd.api.types.is_datetime64_any_dtype(dtype):
                    columns.append(f"{column} DATETIME")
                else:
                    columns.append(f"{column} VARCHAR(255)")
            columns_str = ", ".join(columns)
            query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})"

            cursor.execute(query)
            print(f"Table '{table_name}' created successfully.")
        except Exception as e:
            print(f"Error creating table: {e}")
        finally:
            cursor.close()

    def insert_data(self, table_name, data_frame):
        """
        Insert data from a pandas DataFrame into a MySQL table.

        :param table_name: Name of the target table.
        :param data_frame: pandas DataFrame containing data to insert.
        """
        cursor = self.get_cursor()
        try:
            # Generate an INSERT INTO statement dynamically
            columns = ", ".join(data_frame.columns)
            placeholders = ", ".join(["%s"] * len(data_frame.columns))
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

            # Convert DataFrame rows into tuples for execution
            data_frame = data_frame.replace({pd.NA: "NULL", "": "NULL", "nan": "NULL", "NaN": "NULL"})

            #data_tuples = [tuple(row) for row in data_frame.replace({pd.NA: np.nan, "": np.nan,"nan": np.nan, "NaN": np.nan}).to_numpy()]
            data_tuples = [tuple(row) for row in data_frame.to_numpy()]
            cursor.executemany(query, data_tuples)
            self.commit()
            print(f"Inserted {cursor.rowcount} rows into '{table_name}'.")
        except Exception as e:
            print(f"Error inserting data: {e}")
        finally:
            cursor.close()


    def insert_with_load_data(self, table_name, data_frame):
        """Insert data using MySQL's LOAD DATA INFILE."""
        #temp_csv_file = "temp.csv"
        temp_csv_file = f"temp_{uuid.uuid4().hex}.csv"

        cursor = self.get_cursor()
        try:
            # Save DataFrame to a temporary CSV file
            data_frame.to_csv(temp_csv_file, index=False, header=False, na_rep="\\N")

            query = f"""
            LOAD DATA LOCAL INFILE '{temp_csv_file}'
            INTO TABLE {table_name}
            FIELDS TERMINATED BY ',' 
            LINES TERMINATED BY '\n'
            ({', '.join(data_frame.columns)});
            """

            cursor.execute(query)
            self.commit()
            print(f"Inserted data into '{table_name}' using LOAD DATA INFILE.")
        except Exception as e:
            print(f"Error using LOAD DATA INFILE: {e}")
        finally:
            if os.path.exists(temp_csv_file):
                os.remove(temp_csv_file)
            cursor.close()

    

    def truncate_table(self, table_name):
        """
        Truncate a MySQL table, removing all data.

        :param table_name: Name of the table to truncate.
        """
        cursor = self.get_cursor()
        try:
            query = f"TRUNCATE TABLE {table_name}"
            cursor.execute(query)
            self.commit()
            print(f"Table '{table_name}' truncated successfully.")
        except Exception as e:
            print(f"Error truncating table: {e}")
        finally:
            cursor.close()
