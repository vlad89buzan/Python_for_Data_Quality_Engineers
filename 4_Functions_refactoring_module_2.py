import random
import string


# Function to generate a random dictionary with sorted keys
def generate_random_dict():
    num_keys = random.randint(3, 5)
    random_dict = {random.choice(string.ascii_lowercase): random.randint(0, 100) for _ in range(num_keys)}
    return dict(sorted(random_dict.items()))


# Function to generate a list of random dictionaries
def generate_dicts_list(num_dicts):
    return [generate_random_dict() for _ in range(num_dicts)]


# Function to collect values from all dictionaries by key
def collect_values_by_key(dicts_list):
    common_dict = {}
    for index, d in enumerate(dicts_list):
        for key, value in d.items():
            common_dict.setdefault(key, []).append((value, index))
    return dict(sorted(common_dict.items()))


# Function to process common_dict and create the final updated dictionary
def create_final_dict(common_dict):
    def process_key(key, values):
        if len(values) == 1:
            return key, values[0][0]
        max_tuple = max(values, key=lambda x: x[0])
        return f'{key}_{max_tuple[1] + 1}', max_tuple[0]

    return dict(sorted(process_key(key, value) for key, value in common_dict.items()))


# Main function to orchestrate the dictionary creation, processing, and final combination
def main():
    num_dicts = random.randint(2, 10)  # Generate random number of dictionaries
    dicts_list = generate_dicts_list(num_dicts)
    print("Generated list of dicts with sorted keys:", dicts_list)

    common_dict = collect_values_by_key(dicts_list)
    print("Common_dict:", common_dict)

    final_dict = create_final_dict(common_dict)
    print("Final sorted combined dict:", final_dict)


if __name__ == "__main__":
    main()
