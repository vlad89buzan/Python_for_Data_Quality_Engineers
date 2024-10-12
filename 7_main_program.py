import os
import datetime
import re
from csv_generator import process_text_file
from letter_statistics import calculate_letter_statistics


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


# Helper function to normalize text from a case-insensitive point of view
def normalize_text(text):
    text = text.lower().strip()  # Convert the whole text to lowercase and remove leading/trailing spaces
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    return text.capitalize()  # Capitalize the first letter of the first word


# News class (inherits from Record)
class News(Record):
    def __init__(self, text, city):
        super().__init__(normalize_text(text))  # Normalize the news text
        self.city = city.title()  # Capitalize city name
        self.date = datetime.datetime.now().strftime("%d/%m/%Y %H.%M")

    def format_record(self):
        return (f"News -------------------------\n"
                f"{self.text}\n"
                f"{self.city}, {self.date}")


# PrivateAd class (inherits from Record)
class PrivateAd(Record):
    def __init__(self, text, expiration_date):
        super().__init__(normalize_text(text))  # Normalize the ad text
        self.expiration_date = expiration_date
        self.days_left = (self.expiration_date - datetime.datetime.now()).days

    def format_record(self):
        return (f"Private Ad ------------------\n"
                f"{self.text}\n"
                f"Actual until: {self.expiration_date.strftime('%d/%m/%Y')}, {self.days_left} days left")

    @staticmethod
    def get_valid_expiration_date():
        while True:
            expiration_date_input = input("Enter expiration date (YYYY-MM-DD): ")
            try:
                expiration_date = datetime.datetime.strptime(expiration_date_input, "%Y-%m-%d")

                # Check if the date is in the past
                if expiration_date < datetime.datetime.now():
                    print("The expiration date is in the past. Please enter a future date.")
                else:
                    return expiration_date
            except ValueError:
                print("Incorrect date format. Please enter the date in the format YYYY-MM-DD (e.g., 2024-12-31).")


# QuoteOfTheDay class (unique record example)
class QuoteOfTheDay(Record):
    def __init__(self, quote, author):
        super().__init__(normalize_text(quote))  # Normalize the quote text
        self.author = author.title()  # Capitalize author name

    def format_record(self):
        return (f"Quote of the day ------------\n"
                f"\"{self.text}\"\n"
                f"- {self.author}")


# Manager class to handle user input and manage records
class NewsFeedManager:
    def add_news(self):
        text = input("Enter news text: ")
        city = input("Enter city: ")
        news = News(text, city)
        news.save()

    def add_private_ad(self):
        text = input("Enter ad text: ")
        expiration_date = PrivateAd.get_valid_expiration_date()
        private_ad = PrivateAd(text, expiration_date)
        private_ad.save()

    def add_quote_of_the_day(self):
        quote = input("Enter the quote: ")
        author = input("Enter the author's name: ")
        quote_of_the_day = QuoteOfTheDay(quote, author)
        quote_of_the_day.save()

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
                self.process_file_records()  # Added option to process records from a file
            elif choice == "5":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please select again.")


# New class to process records from a file
class FileProcessor:
    def __init__(self, file_path=None):
        self.file_path = file_path or "news_feed_input.txt"  # Default folder or provided file path

    def process_file(self):
        try:
            with open(self.file_path, "r") as file:
                for line in file:
                    # Assuming each line contains: <type>: <text>; [city|author|expiration_date]
                    # Normalize the record type to lowercase
                    record_type, details = line.strip().split(": ", 1)
                    record_type = record_type.lower()  # Convert to lowercase for case-insensitive matching

                    if record_type == "news":
                        text, city = details.split("; ")
                        news = News(text, city)
                        news.save()
                    elif record_type == "privatead":
                        text, expiration_date_str = details.split("; ")
                        expiration_date = datetime.datetime.strptime(expiration_date_str, "%Y-%m-%d")
                        private_ad = PrivateAd(text, expiration_date)
                        private_ad.save()
                    elif record_type == "quoteoftheday":
                        quote, author = details.split("; ")
                        quote_of_the_day = QuoteOfTheDay(quote, author)
                        quote_of_the_day.save()
                    else:
                        print(f"Unknown record type: {record_type}")

            # If everything is processed successfully, remove the file
            os.remove(self.file_path)
            print(f"File {self.file_path} processed and removed successfully.")

        except FileNotFoundError:
            print(f"File {self.file_path} not found.")
        except Exception as e:
            print(f"An error occurred while processing the file: {e}")


# Main code to start the application
if __name__ == "__main__":
    manager = NewsFeedManager()
    manager.run()
    process_text_file("news_feed_output.txt", "word_count.csv")
    calculate_letter_statistics("news_feed_output.txt")
