# Import the random module to generate random numbers
import random

# Generate a list of 100 random numbers between 0 and 1000
numbers = [random.randint(0, 1000) for i in range(100)]


# Function to sort a list using the bubble sort algorithm
def bubble_sort(arr):
    n = len(arr)  # Determine the number of elements in the array
    for i in range(n):
        # The outer loop ensures that the largest unsorted element "bubbles up" to its correct position in each pass
        for j in range(0, n - i - 1):
            # The inner loop performs the comparison and potential swap of adjacent elements
            if arr[j] > arr[j + 1]:
                # Swap if the element found is greater than the next element
                arr[j], arr[j + 1] = arr[j + 1], arr[j]


# Sort the list from min to max using bubble sort
bubble_sort(numbers)

# Initialize sums and counters for even and odd numbers
even_sum = 0
even_count = 0
odd_sum = 0
odd_count = 0

# Iterate through the sorted list and calculate sums and counts
for num in numbers:
    if num % 2 == 0:
        even_sum += num
        even_count += 1
    else:
        odd_sum += num
        odd_count += 1

# Calculate averages for even and odd numbers
# handling division on zero: if even_count > 0 then even_average else 0;if odd_count > 0 then odd_average else 0
even_average = even_sum / even_count if even_count > 0 else 0
odd_average = odd_sum / odd_count if odd_count > 0 else 0

# Print the results to the console
print(f'Even numbers average: {even_average}')
print(f'Odd numbers average: {odd_average}')
