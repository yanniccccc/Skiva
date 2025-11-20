from mutagen.oggvorbis import OggVorbis
import json 
import os

song_name = "somesong"
song_description = "A cool custom song"

audio = OggVorbis("song.ogg")
duration_seconds = audio.info.length
print(duration_seconds)

dp_data = {
  "comparator_output": 12,
  "description": song_description,
  "length_in_seconds": duration_seconds,
  "sound_event": {
    "sound_id": "custom_music:" + song_name,
  }
}

rp_data = {
  song_name: {
    "sounds": ["custom_music:records/" + song_name]
  }
}


try:
    with open(song_name + ".json", "w") as json_file:
        json.dump(dp_data, json_file, indent=4)
    print("JSON file " + song_name + "'.json' created successfully.")
except IOError as e:
    print(f"Error writing to file: {e}")

try:
    with open("rp.json", "w") as json_file:
        json.dump(rp_data, json_file, indent=4)
    print("JSON file 'rp.json' created successfully.")
except IOError as e:
    print(f"Error writing to file: {e}")

try:
    os.rename("song.ogg", song_name + ".ogg")
    print(f"File '{"song.ogg"}' renamed to '{song_name + ".ogg"}' successfully.")
except FileNotFoundError:
    print(f"Error: The file '{"song.ogg"}' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")