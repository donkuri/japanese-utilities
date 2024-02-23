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
