import re

# Function to normalize header (capitalize first letter)
def normalize_header(text):
    return text.split(':\n\t')[0].capitalize()

# Function to normalize the body text (capitalize first letter of each sentence)
def normalize_body(text):
    body = text.split(':\n\t')[1]
    sentences = body.split('\n\t')
    return '\n\t'.join('. '.join([s.capitalize() for s in sentence.split('. ')]) for sentence in sentences)

# Function to extract the last word from each sentence
def extract_last_words(normalized_text):
    sentences = normalized_text.splitlines()
    return [sentence.split()[-1][:-1] for sentence in sentences if sentence.split()]

# Function to insert a new sentence made of last words into the second paragraph
def insert_new_sentence(sentences, new_sentence):
    if len(sentences) >= 2:
        sentences[2] += ' ' + new_sentence
    return sentences

# Function to fix "iZ" to "is" where it's a mistake using regex
def fix_iz(text):
    return re.sub(r'(?<=\s)iz(?=\s)', 'is', text)

# Function to count all types of whitespace characters in a text
def count_whitespace(text):
    return sum(1 for char in text if char.isspace())

# Main function to orchestrate the normalization, correction, and counting
def main():
    text = '''homEwork:
	tHis iz your homeWork, copy these Text to variable. 

	You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

	it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE. 

	last iz TO calculate nuMber OF Whitespace characteRS in this Text. caREFULL, not only Spaces, but ALL whitespaces. I got 87.
'''

    # Normalize text
    normalized_header = normalize_header(text)
    normalized_body = normalize_body(text)
    normalized_text = ':\n'.join([normalized_header, normalized_body])
    print(f'normalized_text: {normalized_text}')

    # Extract last words and insert into the second paragraph
    last_words = extract_last_words(normalized_body)
    new_sentence = ' '.join(last_words) + '.'
    sentences = normalized_body.splitlines()
    updated_sentences = insert_new_sentence(sentences, new_sentence)
    updated_text = normalized_header + ':\n' + '\n'.join(updated_sentences)
    print(f'updated_text: {updated_text}')

    # Fix "iZ" mistakes
    fixed_iz_text = fix_iz(updated_text)
    print(f'fixed_iz_text: {fixed_iz_text}')

    # Count whitespace characters
    whitespace_count = count_whitespace(text)
    print(f'whitespace_count: {whitespace_count}')


if __name__ == "__main__":
    main()
