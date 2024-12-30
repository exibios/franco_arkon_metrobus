import mysql.connector

class MySQLDriver:
    def __init__(self, host, user, password, database, port=3306):
        """Initialize the database connection parameters."""
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.conn = None
        self.port = port

    def connect(self):
        """Establish a connection to the MySQL database."""
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port,
                allow_local_infile=True
            )
            print("Connected to the database successfully.")
        except mysql.connector.Error as err:
            print(f"Connection error: {err}")
            self.conn = None

    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()
            print("Database connection closed.")

    def get_cursor(self):
        """Return a cursor object for database operations."""
        if self.conn:
            return self.conn.cursor()
        else:
            raise Exception("Database connection is not established.")

    def commit(self):
        """Commit the current transaction."""
        if self.conn:
            self.conn.commit()
