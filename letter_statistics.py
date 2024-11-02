import csv
from collections import Counter


def calculate_letter_statistics(file_path):
    # Initialize counters for all letters and uppercase letters
    letter_counter = Counter()
    uppercase_counter = Counter()

    try:
        # Read the input file
        with open(file_path, 'r') as file:
            text = file.read()  # Read original text to keep uppercase letters

            # Count all letters and uppercase letters
            for char in text:
                if char.isalpha():  # Check if the character is a letter
                    letter_counter[char.lower()] += 1  # Count lowercase letters
                    uppercase_counter[char] += 1 if char.isupper() else 0  # Count uppercase letters

        # Prepare data for CSV output
        total_letters = sum(letter_counter.values())
        statistics = []

        for letter, count_all in letter_counter.items():
            count_uppercase = uppercase_counter.get(letter.upper(), 0)  # Get count of uppercase letters
            percentage = round((count_all / total_letters) * 100, 2) if total_letters > 0 else 0
            statistics.append({
                'letter': letter,
                'count_all': count_all,
                'count_uppercase': count_uppercase,
                'percentage': percentage
            })

        # Write the statistics to a CSV file
        with open('letter_statistics.csv', 'w', newline='') as csvfile:
            fieldnames = ['letter', 'count_all', 'count_uppercase', 'percentage']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(statistics)

        print("Letter statistics generated successfully in letter_statistics.csv.")

    except FileNotFoundError:
        print(f"File {file_path} not found.")
    except Exception as e:
        print(f"An error occurred while processing the file: {e}")


# Example of how to use the function (you can remove this before production)
if __name__ == "__main__":
    calculate_letter_statistics("news_feed_output.txt")  # Call with the output text file path
