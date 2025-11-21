from mutagen.oggvorbis import OggVorbis
import json 
import os
import shutil

def temp():
    song_name = "nullkommaneun-ssio"

    

    rp_data = {
    song_name: {
        "sounds": ["custom_music:records/" + song_name]
    }
    }

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


def write_dp_json(dp_path, song_path, song_name):
    audio = OggVorbis(song_path)
    duration_seconds = audio.info.length
    print(duration_seconds)

    dp_data = {
        "comparator_output": 12,
        "description": song_name,
        "length_in_seconds": duration_seconds,
        "sound_event": {
            "sound_id": "custom_music:" + song_name,
        }
    }

    try:
        with open(os.path.join(dp_path, "data/custom_music/jukebox_song", song_name + ".json"), "w") as json_file:
            json.dump(dp_data, json_file, indent=4)
        print("JSON file " + song_name + "'.json' created successfully.")
    except IOError as e:
        print(f"Error writing to file: {e}")
    


def read_dp_json(path):
    try:
        with open(path, 'r') as file:
            print("Reading file: ", path)
            data = json.load(file)
        return data
    except FileNotFoundError:
        print("Error: file not found.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in file.")

def write_rp_json(rp_path, song_name):
    current_data = {}
    try:
        with open(os.path.join(rp_path, "assets/custom_music/sounds.json"), 'r') as file:
            current_data = json.load(file)
    except FileNotFoundError:
        print("Error: file not found.")
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in file.")
    
    new_song = {
        song_name: {
            "sounds": ["custom_music:records/" + song_name]
        }
    }

    current_data.update(new_song)
    
    try:
        with open(os.path.join(rp_path, "assets/custom_music/sounds.json"), "w") as json_file:
            json.dump(current_data, json_file, indent=4)
        print("JSON file 'sounds.json' successully updated.")
    except IOError as e:
        print(f"Error writing to file: {e}")



def copy_song_to_rp(rp_path, song_path, song_name):
    destination_path = os.path.join(rp_path, "assets/custom_music/sounds/records/", song_name + ".ogg")
    try:
        shutil.copy(song_path, destination_path)
        print(f"File '{song_path}' copied and renamed to '{destination_path}' successfully.")
    except FileNotFoundError:
        print(f"Error: Source file '{song_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def write_creeper_loot_table(dp_path, song_name):
    creeper_loottable_path = os.path.join(dp_path, "data/minecraft/loot_table/entities/creeper.json")
    creeper_loottable = read_dp_json(creeper_loottable_path)
    
    new_entry = {
          "type": "minecraft:item",
          "name": "minecraft:music_disc_5",
          "functions": [
            {
              "function": "minecraft:set_components",
              "components": {
                "minecraft:jukebox_playable": "custom_music:" + song_name
              }
            }
          ]
        }


    if "pools" in creeper_loottable and len(creeper_loottable["pools"]) > 0:
        creeper_loottable["pools"][1]["entries"].append(new_entry)
    else:
        print("Error: Invalid creeper loot table structure.")
        return
    
    try:
        with open(creeper_loottable_path, "w") as json_file:
            json.dump(creeper_loottable, json_file, indent=4)
        print("Creeper loot table updated successfully.")
    except IOError as e:
        print(f"Error writing to file: {e}")