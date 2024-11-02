import sqlite3

def select_all_cities(db_name='cities.db'):
    """Select all records from the city_coordinates table."""
    try:
        with sqlite3.connect(db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM city_coordinates')
            cities = cursor.fetchall()

            if cities:
                print("City Coordinates:")
                for city in cities:
                    print(f"ID:{city[0]} ,City: {city[1]}, Latitude: {city[2]}, Longitude: {city[3]}")
            else:
                print("No cities found in the database.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    select_all_cities()
