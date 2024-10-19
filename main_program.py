import os
import datetime
import re
import json
import xml.etree.ElementTree as ET
import pyodbc
from abc import ABC, abstractmethod
from pathlib import Path
from csv_generator import process_text_file
from letter_statistics import calculate_letter_statistics

db_fn = Path("news_feed.db")


# Base class for all record types
class Record:
    def __init__(self, text):
        self.text = text

    def format_record(self):
        raise NotImplementedError("Subclass must implement this method")

    def save(self):
        with open("news_feed_output.txt", "a") as file:
            file.write(self.format_record() + "\n\n")
        print(f"{self.__class__.__name__} added successfully.")


# Helper function to normalize text
def normalize_text(text):
    text = text.lower().strip()  # Convert to lowercase and strip spaces
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    return text.capitalize()  # Capitalize the first letter


# Database Manager class
class DatabaseManager:
    def __init__(self):
        self.db_file = db_fn
        self.connection_string = f'DRIVER={{SQLite3 ODBC Driver}};DATABASE={self.db_file}'
        self.conn = pyodbc.connect(self.connection_string)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        try:
            create_news_table = '''
                CREATE TABLE IF NOT EXISTS news (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    city TEXT NOT NULL,
                    date TEXT NOT NULL,
                    UNIQUE(text, city, date)
                );
            '''
            self.cursor.execute(create_news_table)

            create_private_ads_table = '''
                CREATE TABLE IF NOT EXISTS private_ads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT NOT NULL,
                    expiration_date TEXT NOT NULL,
                    days_left INTEGER NOT NULL,
                    UNIQUE(text, expiration_date)
                );
            '''
            self.cursor.execute(create_private_ads_table)

            create_quotes_table = '''
                CREATE TABLE IF NOT EXISTS quotes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    quote TEXT NOT NULL,
                    author TEXT NOT NULL,
                    UNIQUE(quote, author)
                );
            '''
            self.cursor.execute(create_quotes_table)

            self.conn.commit()
        except Exception as e:
            print(f"Error creating tables: {e}")

    def save_record(self, table, data):
        try:
            # Check for existing record based on the table
            if table == "news":
                check_query = f"""
                            SELECT COUNT(*) FROM {table}
                            WHERE text = ? AND city = ?  
                        """
                self.cursor.execute(check_query, (data["text"], data["city"]))
                exists = self.cursor.fetchone()[0]

                if exists:
                    print(f"Record already exists in {table}. Record not inserted.")
                    return  # Exit the method if the record already exists

            elif table == "private_ads":
                check_query = f"""
                            SELECT COUNT(*) FROM {table}
                            WHERE text = ? AND expiration_date = ?
                        """
                self.cursor.execute(check_query, (data["text"], data["expiration_date"]))
                exists = self.cursor.fetchone()[0]

                if exists:
                    print(f"Record already exists in {table}. Record not inserted.")
                    return  # Exit the method if the record already exists

            elif table == "quotes":
                check_query = f"""
                            SELECT COUNT(*) FROM {table}
                            WHERE quote = ? AND author = ?
                        """
                self.cursor.execute(check_query, (data["quote"], data["author"]))
                exists = self.cursor.fetchone()[0]

                if exists:
                    print(f"Record already exists in {table}. Record not inserted.")
                    return  # Exit the method if the record already exists

            placeholders = ', '.join(['?'] * len(data))
            query = f"INSERT INTO {table} ({', '.join(data.keys())}) VALUES ({placeholders})"
            self.cursor.execute(query, tuple(data.values()))
            self.conn.commit()
            print(f"Record inserted into {table}")
        except pyodbc.IntegrityError:
            print(f"Duplicate record found in {table}. Record not inserted.")

    def close_connection(self):
        self.conn.close()


# News class
class News(Record):
    def __init__(self, text, city):
        super().__init__(normalize_text(text))
        self.city = city.title()
        self.date = datetime.datetime.now().strftime("%d/%m/%Y %H.%M")

    def format_record(self):
        return (f"News -------------------------\n"
                f"{self.text}\n"
                f"{self.city}, {self.date}")

    def save_to_db(self):
        db_manager = DatabaseManager()
        data = {
            "text": self.text,
            "city": self.city,
            "date": self.date
        }
        db_manager.save_record("news", data)
        db_manager.close_connection()


# PrivateAd class
class PrivateAd(Record):
    def __init__(self, text, expiration_date):
        super().__init__(normalize_text(text))
        self.expiration_date = expiration_date
        self.days_left = (self.expiration_date - datetime.datetime.now()).days

    def format_record(self):
        return (f"Private Ad ------------------\n"
                f"{self.text}\n"
                f"Actual until: {self.expiration_date.strftime('%d/%m/%Y')}, {self.days_left} days left")

    def save_to_db(self):
        db_manager = DatabaseManager()
        data = {
            "text": self.text,
            "expiration_date": self.expiration_date.strftime('%Y-%m-%d'),
            "days_left": self.days_left
        }
        db_manager.save_record("private_ads", data)
        db_manager.close_connection()

    @staticmethod
    def get_valid_expiration_date():
        while True:
            expiration_date_input = input("Enter expiration date (YYYY-MM-DD): ")
            try:
                expiration_date = datetime.datetime.strptime(expiration_date_input, "%Y-%m-%d")
                if expiration_date < datetime.datetime.now():
                    print("The expiration date is in the past. Please enter a future date.")
                else:
                    return expiration_date
            except ValueError:
                print("Incorrect date format. Please enter the date in the format YYYY-MM-DD (e.g., 2024-12-31).")


# QuoteOfTheDay class
class QuoteOfTheDay(Record):
    def __init__(self, quote, author):
        super().__init__(normalize_text(quote))
        self.author = author.title()

    def format_record(self):
        return (f"Quote of the day ------------\n"
                f"\"{self.text}\"\n"
                f"- {self.author}")

    def save_to_db(self):
        db_manager = DatabaseManager()
        data = {
            "quote": self.text,
            "author": self.author
        }
        db_manager.save_record("quotes", data)
        db_manager.close_connection()


# Manager class for user input
class NewsFeedManager:
    def add_news(self):
        text = input("Enter news text: ")
        city = input("Enter city: ")
        news = News(text, city)
        news.save()
        news.save_to_db()

    def add_private_ad(self):
        text = input("Enter ad text: ")
        expiration_date = PrivateAd.get_valid_expiration_date()
        private_ad = PrivateAd(text, expiration_date)
        private_ad.save()
        private_ad.save_to_db()

    def add_quote_of_the_day(self):
        quote = input("Enter the quote: ")
        author = input("Enter the author's name: ")
        quote_of_the_day = QuoteOfTheDay(quote, author)
        quote_of_the_day.save()
        quote_of_the_day.save_to_db()

    def process_file_records(self):
        file_path = input("Enter the file path (or press Enter for default): ")
        file_processor = FileProcessor(file_path if file_path else None)
        file_processor.process_file()

    def run(self):
        while True:
            print("Select a record type to add:")
            print("1. News")
            print("2. Private Ad")
            print("3. Quote of the Day")
            print("4. Process records from file")
            print("5. Exit")

            choice = input("Enter your choice (1/2/3/4/5): ")

            if choice == "1":
                self.add_news()
            elif choice == "2":
                self.add_private_ad()
            elif choice == "3":
                self.add_quote_of_the_day()
            elif choice == "4":
                self.process_file_records()
            elif choice == "5":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please select again.")


# Abstract base class for file processors
class BaseFileProcessor(ABC):
    def __init__(self, file_path: str):
        self.file_path = file_path

    @abstractmethod
    def process_file(self):
        pass

    def read_file(self):
        try:
            with open(self.file_path, "r") as file:
                return file.read()
        except FileNotFoundError:
            print(f"File {self.file_path} not found.")
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")
            return None


# Specific class to process text (.txt) files
class TextFileProcessor(BaseFileProcessor):
    def process_file(self):
        file_content = self.read_file()
        if file_content is None:
            return

        for line in file_content.strip().split("\n"):
            record_type, details = line.split(": ", 1)
            record_type = record_type.lower()

            if record_type == "news":
                text, city = details.split("; ")
                News(text, city).save()
                News(text, city).save_to_db()
            elif record_type == "privatead":
                text, expiration_date_str = details.split("; ")
                expiration_date = datetime.datetime.strptime(expiration_date_str, "%Y-%m-%d")
                PrivateAd(text, expiration_date).save()
                PrivateAd(text, expiration_date).save_to_db()
            elif record_type == "quoteoftheday":
                quote, author = details.split("; ")
                QuoteOfTheDay(quote, author).save()
                QuoteOfTheDay(quote, author).save_to_db()
            else:
                print(f"Unknown record type: {record_type}")
        os.remove(self.file_path)
        print(f"File {self.file_path} processed and removed.")


# Specific class to process JSON (.json) files
class JsonFileProcessor(BaseFileProcessor):
    def process_file(self):
        file_content = self.read_file()
        if file_content is None:
            return

        try:
            data = json.loads(file_content)
            for record in data["records"]:
                record_type = record["type"].lower()

                if record_type == "news":
                    News(record["text"], record["city"]).save()
                    News(record["text"], record["city"]).save_to_db()
                elif record_type == "privatead":
                    expiration_date = datetime.datetime.strptime(record["expiration_date"], "%Y-%m-%d")
                    PrivateAd(record["text"], expiration_date).save()
                    PrivateAd(record["text"], expiration_date).save_to_db()
                elif record_type == "quoteoftheday":
                    QuoteOfTheDay(record["quote"], record["author"]).save()
                    QuoteOfTheDay(record["quote"], record["author"]).save_to_db()
                else:
                    print(f"Unknown record type: {record_type}")

            os.remove(self.file_path)
            print(f"File {self.file_path} processed and removed.")
        except json.JSONDecodeError:
            print("Error decoding JSON. Please check the file format.")
        except Exception as e:
            print(f"An error occurred while processing the JSON file: {e}")


# Specific class to process XML (.xml) files
class XmlFileProcessor(BaseFileProcessor):
    def process_file(self):
        file_content = self.read_file()
        if file_content is None:
            return

        try:
            root = ET.fromstring(file_content)
            for record in root.findall('record'):
                record_type = record.get('type').lower()

                if record_type == "news":
                    text = record.find('text').text
                    city = record.find('city').text
                    News(text, city).save()
                    News(text, city).save_to_db()
                elif record_type == "privatead":
                    text = record.find('text').text
                    expiration_date_str = record.find('expiration_date').text
                    expiration_date = datetime.datetime.strptime(expiration_date_str, "%Y-%m-%d")
                    PrivateAd(text, expiration_date).save()
                    PrivateAd(text, expiration_date).save_to_db()
                elif record_type == "quoteoftheday":
                    quote = record.find('quote').text
                    author = record.find('author').text
                    QuoteOfTheDay(quote, author).save()
                    QuoteOfTheDay(quote, author).save_to_db()
                else:
                    print(f"Unknown record type: {record_type}")

            os.remove(self.file_path)
            print(f"File {self.file_path} processed and removed.")
        except ET.ParseError:
            print("Error parsing XML. Please check the file format.")
        except Exception as e:
            print(f"An error occurred while processing the XML file: {e}")


# File processor that delegates to specific file types
class FileProcessor:
    """Class responsible for processing files based on their format."""

    def __init__(self, file_path: str):
        self.file_path = file_path or "news_feed_input.json"

    def process_file(self):
        _, file_extension = os.path.splitext(self.file_path)

        if file_extension.lower() == ".txt":
            processor = TextFileProcessor(self.file_path)
        elif file_extension.lower() == ".json":
            processor = JsonFileProcessor(self.file_path)
        elif file_extension.lower() == ".xml":
            processor = XmlFileProcessor(self.file_path)
        else:
            print(f"Unsupported file extension: {file_extension}. Only .txt, .json, and .xml are supported.")
            return

        processor.process_file()


# Main execution point
if __name__ == "__main__":
    manager = NewsFeedManager()
    manager.run()
    process_text_file("news_feed_output.txt", "word_count.csv")
    calculate_letter_statistics("news_feed_output.txt")
