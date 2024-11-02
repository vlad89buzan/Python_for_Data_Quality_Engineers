import pyodbc

# Database file name
db_fn = "news_feed.db"

# Database Manager class
class DatabaseManager:
    def __init__(self):
        self.connection_string = f'DRIVER={{SQLite3 ODBC Driver}};DATABASE={db_fn}'
        self.conn = pyodbc.connect(self.connection_string)
        self.cursor = self.conn.cursor()

    def get_all_records(self):
        tables = ['news', 'private_ads', 'quotes']
        for table in tables:
            print(f"Records from {table} table:")
            query = f"SELECT * FROM {table};"
            self.cursor.execute(query)
            rows = self.cursor.fetchall()
            for row in rows:
                print(row)
            print("\n")  # Separate tables with a newline

    def close_connection(self):
        self.conn.close()


# Main execution point
if __name__ == "__main__":
    db_manager = DatabaseManager()
    db_manager.get_all_records()
    db_manager.close_connection()
