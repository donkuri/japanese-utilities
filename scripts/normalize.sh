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
