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
