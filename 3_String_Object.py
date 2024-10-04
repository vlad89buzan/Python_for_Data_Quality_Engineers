import re

#  Copy the text to a variable
text = '''homEwork:
	tHis iz your homeWork, copy these Text to variable. 

	You NEED TO normalize it fROM letter CASEs point oF View. also, create one MORE senTENCE witH LAST WoRDS of each existING SENtence and add it to the END OF this Paragraph.

	it iZ misspeLLing here. fix“iZ” with correct “is”, but ONLY when it Iz a mistAKE. 

	last iz TO calculate nuMber OF Whitespace characteRS in this Text. caREFULL, not only Spaces, but ALL whitespaces. I got 87.
'''

# Normalize letter cases (capitalize first letter of sentences, make the rest lowercase)

normalized_text1 = text.split(':\n\t')[0].capitalize()  # Normalize the header
text2 = text.split(':\n\t')[1]  # Extract the body text
normalized_text2 = ''
for sentence in text2.split('\n\t'):  # Split the body into sentences
    str = '. '.join([s.capitalize() for s in sentence.split('. ')])  # Capitalize each sentence
    normalized_text2 = normalized_text2 + str  # Append to normalized_text2
normalized_text = ':\n'.join([normalized_text1, normalized_text2])  # Combine header and normalized body

# Extract the last word from each sentence
last_words = []  # Initialize list to store last words
sentences = normalized_text2.splitlines()  # Split normalized text into lines
for sentence in sentences:
    words = sentence.split()  # Split sentence into words
    if words:  # Make sure the sentence isn't empty
        last_word = words[-1][:-1]  # Remove the last character from the last word, because it is '.'
        last_words.append(last_word)  # Append the last word to the list
new_sentence = ' '.join(last_words) + '.'  # Join last words to create a new sentence

# Insert the new sentence at the end of the second paragraph
if len(sentences) >= 2:  # Check if there is a second line
    sentences[1] += ' ' + new_sentence  # Append new_sentence to the second line
# Join the sentences back into a single text
updated_text = normalized_text1 + ':\n' + '\n'.join(sentences)  # Combine header with updated sentences

# Fix "iZ" where it's incorrect using regex
fixed_iz_text = re.sub(r'(?<=\s)iz(?=\s)', 'is', updated_text)  # Replace "iz" with "is" in specific contexts

# Count all types of whitespace characters in the original text
whitespace_count = sum(1 for char in text if char.isspace())  # Count whitespace characters

# Print the results
print(f'normalized_text: {normalized_text}')
print(f'updated_text: {updated_text}')
print(f'fixed_iz_text: {fixed_iz_text}')
print(f'whitespace_count: {whitespace_count}')

