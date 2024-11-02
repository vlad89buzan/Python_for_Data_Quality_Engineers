import sqlite3
import math


class CityDatabase:
    def __init__(self, db_name='cities.db'):
        self.db_name = db_name
        self.create_db()

    def create_db(self):
        """Create SQLite database and table if it doesn't exist."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS city_coordinates (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    city_name TEXT,
                    latitude REAL,
                    longitude REAL
                )
            ''')
            conn.commit()

    def get_coordinates(self, city_name):
        """Retrieve all coordinates for a given city name."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT id, latitude, longitude FROM city_coordinates WHERE city_name = ? COLLATE NOCASE',
                           (city_name,))
            return cursor.fetchall()  # Fetch all matching rows

    def store_coordinates(self, city_name, latitude, longitude):
        """Store the coordinates of a city in the database."""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            # Capitalize each word in the city name before storing it
            cursor.execute('INSERT OR REPLACE INTO city_coordinates (city_name, latitude, longitude) VALUES (?, ?, ?)',
                           (city_name.title(), latitude, longitude))
            conn.commit()


class DistanceCalculator:
    EARTH_RADIUS_KM = 6371.0  # Radius of Earth in kilometers

    @staticmethod
    def haversine(lat1, lon1, lat2, lon2):
        """Calculate the great-circle distance between two points on the Earth."""
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)

        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        a = (math.sin(dlat / 2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) *
             math.sin(dlon / 2) ** 2)
        c = 2 * math.asin(math.sqrt(a))

        return DistanceCalculator.EARTH_RADIUS_KM * c


class CityDistanceTool:
    def __init__(self):
        self.db = CityDatabase()

    def run(self):
        city1 = input("Enter the first city name: ").title()
        city2 = input("Enter the second city name: ").title()

        # Get or confirm coordinates for each city
        lat1, lon1 = self.get_city_coordinates(city1)
        lat2, lon2 = self.get_city_coordinates(city2)

        # Calculate and display the distance
        distance = DistanceCalculator.haversine(lat1, lon1, lat2, lon2)
        print(f"The straight-line distance between {city1} and {city2} is {distance:.2f} km.")

    def get_city_coordinates(self, city_name):
        """Retrieve or prompt for city coordinates, with selection if multiple entries exist."""
        coords_list = self.db.get_coordinates(city_name)
        if coords_list:
            print(f"Found {len(coords_list)} coordinate(s) for {city_name} in the database.")
            for i, (id, lat, lon) in enumerate(coords_list, start=1):
                print(f"{i}. Latitude: {lat}, Longitude: {lon}")

            choice = input("Choose an option by number or enter 'new' to add new coordinates: ").strip().lower()
            if choice.isdigit() and 1 <= int(choice) <= len(coords_list):
                chosen_coords = coords_list[int(choice) - 1][1:]  # Get the (latitude, longitude) part
                return chosen_coords
            elif choice == 'new':
                return self.add_new_city_coordinates(city_name)
            else:
                print("Invalid choice. Please try again.")
                return self.get_city_coordinates(city_name)
        else:
            # No existing records; add new coordinates
            return self.add_new_city_coordinates(city_name)

    def add_new_city_coordinates(self, city_name):
        """Prompt for new coordinates in decimal degrees and store them in the database."""
        print(f"Adding new coordinates for {city_name}.")
        lat = self.get_coordinate("latitude")
        lon = self.get_coordinate("longitude")
        self.db.store_coordinates(city_name, lat, lon)
        return lat, lon

    def get_coordinate(self, coord_type):
        """Get user input for latitude or longitude in decimal degrees format."""
        while True:
            try:
                coord = float(input(f"Enter {coord_type} in decimal degrees (e.g., 50.450001): "))
                # Validate latitude and longitude ranges
                if coord_type == "latitude" and not (-90 <= coord <= 90):
                    raise ValueError("Latitude must be between -90 and 90 degrees.")
                elif coord_type == "longitude" and not (-180 <= coord <= 180):
                    raise ValueError("Longitude must be between -180 and 180 degrees.")
                return coord
            except ValueError:
                print(f"Invalid input. Please enter {coord_type} as a number in decimal degrees.")



if __name__ == "__main__":
    tool = CityDistanceTool()
    tool.run()
