import csv
import os
import pykakasi

# Prompt the user to input the field names
word_field = input("Enter the name of the field for the word: ")
reading_field = input("Enter the name of the field for the reading: ")
sentence_field = input("Enter the name of the field for the sentence: ")

# Prompt the user to input the path and name of the input deck file
input_file = input("Enter the full path (name included) to the input deck file: ")

# Prompt the user to input the path and name of the output deck file
output_file = input("Enter the full path (name included) where you want the output deck file to be saved: ")

kakasi = pykakasi.kakasi()
# Open the original CSV file with tab delimiter
with open(input_file, 'r', newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile, delimiter='\t')
    fieldnames = reader.fieldnames

    # Create a new CSV file for writing the modified data
    with open(output_file, 'w', newline='', encoding='utf-8') as modified_csvfile:
        writer = csv.DictWriter(modified_csvfile, fieldnames=fieldnames, delimiter='\t')
        
        # Write the header row
        writer.writeheader()
        
        # Iterate through each row in the CSV (excluding header row)
        for row in reader:
            word = row[word_field]
            reading = row[reading_field]
            sentence = row[sentence_field]

            modified_sentence = sentence.replace(f'<b>{word}</b>', f'<u>{reading}</u>')
            # If replace failed convert it to hiragana
            if modified_sentence == sentence:
                segments = sentence.split('<b>')
                converted_segments = [segments[0]]
                for segment in segments[1:]:
                    word, remaining = segment.split('</b>', 1)
                    hiraganas = [conversion['hira'] for conversion in kakasi.convert(word)]
                    hiraganas = ''.join(hiraganas)
                    converted_segments.append(f'<u>{hiraganas}</u>{remaining}')
                modified_sentence = ''.join(converted_segments)

            
            # Update the 'Sentence' field in the row
            row[sentence_field] = modified_sentence
            
            # Write the modified row to the new CSV file
            writer.writerow(row)
            
print("Modified CSV file created successfully!")
