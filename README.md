# japanese-utilities
Miscellaneous scripts and the like that help with Japanese learning in some capacity.

## Bash scripts

Various bash scripts that I have used to make Anki decks better.

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
