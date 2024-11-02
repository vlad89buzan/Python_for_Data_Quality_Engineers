import re
import csv
from collections import Counter



def process_text_file(input_file, output_csv):
    # Initialize a Counter to store word counts
    word_count = Counter()

    try:
        # Read the contents of the input file
        with open(input_file, "r") as file:
            text = file.read()

        # Normalize the text: convert to lowercase and remove punctuation
        words = re.findall(r'\b\w+\b', text.lower())  # Extract words using regex
        word_count.update(words)  # Update the word count with the list of words

        # Write the word counts to a CSV file
        with open(output_csv, "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Word", "Count"])  # CSV header
            for word, count in word_count.items():
                writer.writerow([word, count])

        print(f"Word counts written to {output_csv}.")

    except FileNotFoundError:
        print(f"File {input_file} not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


# Example usage
if __name__ == "__main__":
    input_file = "news_feed_output.txt"  # Change to your output file name
    output_csv = "word_count.csv"  # CSV file to write word counts
    process_text_file(input_file, output_csv)
