# japanese-utilities
Miscellaneous scripts and the like that help with Japanese learning in some capacity.

## Scripts

There are two kinds of scripts: Bash scripts and Python scripts. Bash scripts are mostly used to fix files in the `collection.media` Anki folder, whereas the Python script here is used to convert Anki decks.

## Python

### Convert decks to a writing format

This script was written with the help of [Kaanium](https://github.com/kaanium). Inspired by [the deck on this page](https://animecards.site/writingjapanese/), I have written a script to turn [Kaishi 1.5k](https://github.com/donkuri/Kaishi/) into a writing deck of a similar format. Roughly speaking, the front of the card is a sentence with the word you are trying to write underlined and in _kana_ script. The back is then the sentence with the right kanji as well as a kanji diagram. Since this script was written with Kaishi and only Kaishi in mind, it will require some modifications to use it if you're using a completely different deck. Here is roughly how to use the script:

#### Steps to get a proper writing deck

1. Make sure your deck has a Word field (this should have the word in kanji), a Sentence field (this should have the sentence in kanji and **the word should be bolded**) and finally a Reading field (this has the word in hiragana). If this isn't the case, the script will most likely not work unless you change it, see below. On top of those three, create a new empty field called `Sentence Original` or something. This is where your old sentence will stay.
2. Export your deck to `.txt` by right-clicking on the cog wheel to the right of the deck, then choosing `Export`. Under `Export format:` choose `Notes in plain text (.txt)`. Then make sure `Include HTML and media references` is ticked on.
3. The `.txt` you receive is not properly formatted for the deck. Open it with your favorite software (Excel, Calc, whatever) and take out the first lines that are not fields of the deck. Usually those are of the form `#something:bla`, for instance `#separator:tab`. Make sure you take out all these lines. Then, on the first line, write down the fields of the deck and separate them with tabs. For instance, `Word    Definition    Reading    Audio    Sentence    Sentence Translation`. **It is crucial that the separation is done with tabs and not spaces, otherwise the script will fail.** After all of this, copy paste the column `Sentence` into `Sentence Original`. This is done to preserve the original sentence somewhere.
4. Run the script in the terminal, and make sure to write down everything properly in the terminal (what the fields' names are, where the file is located and what its name is). If there is an error somewhere, the script will fail.
5. You should now have a `.txt` file that can be imported back into Anki, but first to avoid any error with your original decks, create a new profile in Anki and create the notetype this deck is supposed to have. This is to avoid having your actual deck be overwritten by the writing deck. To do this, go on the top left `File > Switch Profile` and then `Add`. After this, create the same notetype and deck by going to `Create Deck` on the bottom. Name your deck what you want and then press `OK`. Then go to `Tools > Manage Note Types`, or press `Ctrl+Shift+N`. Click `Add > Add: Basic` and name it appropriately. Once this is done, open the Note Types window again (same thing as before), select your Note Type and click on `Fields`. From there, write down the fields as they are on your deck.
6. Import the `.txt` file by clicking `Import File` on the bottom. **Make sure you choose the right Note Type and the right Deck to import on top of**. You should now have your deck formatted just right.
7. Optionally, use [Kanji Colorizer](https://github.com/cayennes/kanji-colorize/) to add kanji diagrams to your deck. If you choose to do so, make sure you have a kanji field, if you don't have one you can create it by copying your Word field and using regex to take out any hiragana. Then add an empty `Diagram` field and make sure there is `japanese` in your deck name. Then run the add-on and it will generate the diagrams for you.
8. Modify your deck's template to fit the writing deck. Personally, I have the `Sentence` in front (the one that has the word underlined in kana), and both the `Original Sentence` and kanji `Diagram` on the back. You're free to play around with the templates yourself, or to change fonts or something.

#### The script itself

Simply save this script to a file ending in `.py` somewhere on your PC, or simply download it from the `Scripts` folder in this repository. Mine is called `to-writing-deck.py`.

```Python
import csv
import os
import pykakasi

# Prompt the user to input the field names
word_field = input("Enter the name of the field for the word: ")
reading_field = input("Enter the name of the field for the reading: ")
sentence_field = input("Enter the name of the field for the sentence: ")

# Prompt the user to input the path and name of the input deck file
input_deck_path = input("Enter the path to the input deck file (CSV with tab separation): ")
input_deck_file = input("Enter the name of the input deck file: ")
input_file = os.path.join(input_deck_path, input_deck_file)

# Prompt the user to input the path and name of the output deck file
output_deck_path = input("Enter the path to save the output deck file (CSV with tab separation): ")
output_deck_file = input("Enter the name of the output deck file: ")
output_file = os.path.join(output_deck_path, output_deck_file)

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
```

#### What to do if your deck isn't formatted right

There are multiple formatting problems that might arise. If you only have a Word Furigana field, with the word in kanji as well as furigana (e.g. 見[み]る), then using the `Find and Replace` function in Anki with regex to take out the kanji and the brackets should do the trick. If you have no bolding on your sentence, things are a bit more complex and you will need to rewrite the portion of the code that modifies the sentence (line 39) and the portion of the code that segments the sentence in case of replacement failure (line 42). If you only have a sentence field and no word field, well, I don't know.

## Bash

### Trim silence

This bash script is used to take out initial silence on `.mp3` files with the help of [FFmpeg](https://ffmpeg.org/). This is especially useful on example sentences audio files that tend to have some extra silent padding at the beginning. This creates new files with "_trimmed" appended at the end of the filename. You need to replace `/path/to/your/folder` with the actual path to your folder.

```bash
#!/bin/bash

# Define the folder containing the audio files
folder="/path/to/your/folder"

# Loop through all files in the folder
for file in "$folder"/*; do
    # Check if the file is an audio file
    if [ -f "$file" ] && [[ "$file" == *.mp3 ]]; then
        # Extract filename without extension
        filename=$(basename "$file" .mp3)
        
        # Remove silence from the beginning of the audio file
        ffmpeg -i "$file" -af silenceremove=1:0:-50dB "$folder/$filename"_trimmed.mp3
        
        # Optional: Remove original file after processing
        # rm "$file"
    fi
done
```
If you would like to immediately rename the files for some reason, I have a script for that too. Here as well you need to replace `/path/to/your/folder` with the path to your folder.

```bash
#!/bin/bash

# Define the folder containing the trimmed audio files
folder="/path/to/your/folder"

# Loop through all files in the folder
for file in "$folder"/*_trimmed.mp3; do
    # Check if the file is an audio file
    if [ -f "$file" ]; then
        # Extract filename without extension
        filename="${file%_trimmed.mp3}"
        
        # Rename the file to remove '_trimmed' from the filename
        mv "$file" "$filename.mp3"
    fi
done
```

### Normalize audio levels across mp3 files

Sometimes when you get audio files for example sentences, the audio levels are all over the place. This script uses [FFmpeg](https://ffmpeg.org/) to normalize the audio levels in the collection folder. Once again, please replace `/path/to/your/folder` with the actual path to your folder. If your files are of a different format, simply replace `.mp3` with the format of your choice, as long as it's supported by FFmpeg.

```bash
#!/bin/bash

# Define the folder containing the audio files
folder="/path/to/your/folder"

# Create a temporary list file to store input file paths
list_file=$(mktemp)

# Loop through all files in the folder and write their paths to the list file
for file in "$folder"/*.mp3; do
    echo "file '$file'" >> "$list_file"
done

# Normalize the audio levels of all files in the list file
ffmpeg -f concat -safe 0 -i "$list_file" -af loudnorm=I=-16:LRA=11:TP=-1.5:print_format=summary -f null -

# Clean up temporary list file
rm "$list_file"
```
