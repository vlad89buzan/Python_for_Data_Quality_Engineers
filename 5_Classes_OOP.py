import datetime


# Base class for all record types
class Record:
    def __init__(self, text):
        self.text = text

    def format_record(self):
        raise NotImplementedError("Subclass must implement this method")

    def save(self):
        with open("news_feed_oop.txt", "a") as file:
            file.write(self.format_record() + "\n\n")
        print(f"{self.__class__.__name__} added successfully.")


# News class (inherits from Record)
class News(Record):
    def __init__(self, text, city):
        super().__init__(text)
        self.city = city
        self.date = datetime.datetime.now().strftime("%d/%m/%Y %H.%M")

    def format_record(self):
        return (f"News -------------------------\n"
                f"{self.text}\n"
                f"{self.city}, {self.date}")


# PrivateAd class (inherits from Record)
class PrivateAd(Record):
    def __init__(self, text, expiration_date):
        super().__init__(text)
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
        super().__init__(quote)
        self.author = author

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

    def run(self):
        while True:
            print("Select a record type to add:")
            print("1. News")
            print("2. Private Ad")
            print("3. Quote of the Day")
            print("4. Exit")

            choice = input("Enter your choice (1/2/3/4): ")

            if choice == "1":
                self.add_news()
            elif choice == "2":
                self.add_private_ad()
            elif choice == "3":
                self.add_quote_of_the_day()
            elif choice == "4":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please select again.")


# Main code to start the application
if __name__ == "__main__":
    manager = NewsFeedManager()
    manager.run()
