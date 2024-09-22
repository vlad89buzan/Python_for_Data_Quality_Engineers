import random  # Import the random module to generate random numbers
import string  # Import the string module to access string constants like lowercase letters

dicts_list = []  # Initialize an empty list to hold the generated dictionaries
num_dicts = random.randint(2, 10)  # Generate a random number of dictionaries (between 2 and 10)

for i in range(num_dicts):  # Loop to create the specified number of dictionaries
    num_keys = random.randint(3, 5)  # Generate a random number of keys for each dictionary (between 3 and 5)
    new_dict = {random.choice(string.ascii_lowercase): random.randint(0, 100) for _ in
                range(num_keys)}  # Create a new dictionary with random keys (letters) and random values (0-100)
    sorted_dict = dict(sorted(new_dict.items()))  # Sort the dictionary by its keys and convert it back to a dictionary
    dicts_list.append(sorted_dict)  # Append the sorted dictionary to the list

print("Generated list of dicts with sorted keys:", dicts_list)  # Display the generated list of dictionaries

common_dict = {}  # Initialize an empty dictionary to hold lists of values for each key

for index, d in enumerate(dicts_list):  # Loop through each dictionary in the list with its index
    for key, value in d.items():  # Loop through each key-value pair in the current dictionary
        if key not in common_dict:  # If the key is not already in common_dict
            common_dict[key] = []  # Initialize it with an empty list
        common_dict[key].append(
            (value, index))  # Append a tuple of (value, index) to the list for the corresponding key
common_dict = dict(
    sorted(common_dict.items()))  # Sort the common dictionary by keys and convert it back to a dictionary
print("Common_dict:", common_dict)  # Display the common dictionary

updated_dict = {}  # Initialize an empty dictionary to hold the updated key-value pairs

for key, value in common_dict.items():  # Loop through each key in the common dictionary
    if len(value) == 1:  # If there's only one value for the key
        updated_dict[key] = value[0][0]  # Store it directly in the updated dictionary
    else:
        max_tuple = max(value, key=lambda x: x[0])  # Find the tuple with the maximum first element
        key = f'{key}_{max_tuple[1] + 1}'  # Rename the key to include the index of the dictionary that had the max
        # value
        updated_dict[key] = max_tuple[0]  # Store the max value with the renamed key

final_dict = dict(
    sorted(updated_dict.items()))  # Sort the updated dictionary by keys and convert it back to a dictionary

print("Final sorted combined dict:", final_dict)  # Display the final sorted combined dictionary
