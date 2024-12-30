import pandas as pd
import os
from mysql_dao import MySQLDAO

def process_zip(zip_path, file_to_process=None):
    # Load the TXT file into a pandas DataFrame
    import zipfile
    with zipfile.ZipFile(zip_path, 'r') as z:
        if file_to_process:  # Process only a specific file
            with z.open(file_to_process) as f:
                df = pd.read_csv(f)
                return df,file_to_process.rsplit(".", 1)[0]
        else:  # Process all files
            for file_name in z.namelist():
                if file_name.endswith('.txt'):  # Filter for txt files
                    with z.open(file_name) as f:
                        df = pd.read_csv(f)
                        print(f"Processing {file_name}")
                        yield df,file_name.rsplit(".", 1)[0]  # Use a generator for lazy loading


def process_file(table_name, db_config,df):
    """
    Process a CSV file: create a MySQL table and insert its data.

    :param file_path: Path to the CSV file.
    :param table_name: Name of the MySQL table.
    :param db_config: Dictionary containing database connection parameters.
    """
    # Initialize the DAO
    dao = MySQLDAO(**db_config)

    # Connect to the database
    dao.connect()

    try:
        
        # Create table and insert data
        dao.create_table(table_name, df)
        #dao.insert_data(table_name, df)
        dao.truncate_table(table_name)
        dao.insert_with_load_data(table_name, df)
    finally:
        # Close the database connection
        dao.close()

if __name__ == "__main__":
    # Database connection configuration
    db_config = {
        "host": "db", #service name in dockercompose
        "user": "franco",
        "password": "francoakronmetrobus",
        "database": "metrobus"
    }

    zip_path = 'Metrobus_GTFS_ESTATICO.zip'
    for df,table_name in process_zip(zip_path):
        print(df.head())  # Process DataFrame chunk by chunk
        process_file(table_name, db_config, df)
