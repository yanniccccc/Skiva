import dearpygui.dearpygui as dpg
from utility import read_dp_json, write_dp_json, write_rp_json, copy_song_to_rp, write_creeper_loot_table
import os

dp_dir_path = ""
rp_dir_path = ""
song_path = ""
creeper_loottable = {}
is_creeper_checked = True

dpg.create_context()

def dp_callback(sender, app_data):
    global dp_dir_path, creeper_loottable
    dp_dir_path = app_data['file_path_name']
    creeper_loottable = read_dp_json(os.path.join(dp_dir_path,"data/minecraft/loot_tables/entities/creeper.json"))
    dpg.set_value("dp_selected_text", f"Selected: {dp_dir_path}")

def dp_cancel_callback(sender, app_data):
    pass

def rp_callback(sender, app_data):
    global rp_dir_path
    rp_dir_path = app_data['file_path_name']
    dpg.set_value("rp_selected_text", f"Selected: {rp_dir_path}")

def rp_cancel_callback(sender, app_data):
    pass

def song_callback(sender, app_data):
    global song_path
    song_path = app_data['file_path_name']
    dpg.set_value("song_selected_text", f"Selected: {song_path}")

def song_cancel_callback(sender, app_data):
    pass

def checkbox_callback(sender, app_data):
    global is_creeper_checked
    is_creeper_checked = app_data

def start_callback():
    song_name = dpg.get_value(input_song_name)
    print("Starting process for song: ", song_name)
    print("Datapack directory: " + dp_dir_path)
    print("Song file path: " + song_path)
    write_dp_json(dp_dir_path, song_path, song_name)
    write_rp_json(rp_dir_path, song_name)
    copy_song_to_rp(rp_dir_path, song_path, song_name)
    if is_creeper_checked:
        write_creeper_loot_table(dp_dir_path, song_name)
    # Here you would call the function to process the song with the given name and dp_dir_path

dpg.add_file_dialog(
    directory_selector=True, show=False, callback=rp_callback, tag="rp_file_dialog_id",
    cancel_callback=rp_cancel_callback, width=700 ,height=400)

dpg.add_file_dialog(
    directory_selector=True, show=False, callback=dp_callback, tag="dp_file_dialog_id",
    cancel_callback=dp_cancel_callback, width=700 ,height=400)

with dpg.file_dialog(directory_selector=False, show=False, callback=song_callback, tag="song_dialog_id", cancel_callback=song_cancel_callback, width=700 ,height=400):
    dpg.add_file_extension(".ogg", color=(150, 255, 150, 255))

with dpg.window(label="Minecraft Custom Disc Maker", tag="Primary Window", width=800, height=450):
    # Datapack Selection Group
    with dpg.group(horizontal=False, horizontal_spacing=10):
        dpg.add_separator()
        dpg.add_text("Step 1: Select the **Datapack** Directory", color=(255, 165, 0))
        dpg.add_button(label="Select Datapack", callback=lambda: dpg.show_item("dp_file_dialog_id"))
        dpg.add_text("Selected: none", tag="dp_selected_text", wrap=750)
    
    dpg.add_spacing(height=15) # Add extra space between groups

    # Resource Pack Selection Group
    with dpg.group(horizontal=False, horizontal_spacing=10):
        dpg.add_separator()
        dpg.add_text("Step 2: Select the **Resourcepack** Directory", color=(0, 191, 255))
        dpg.add_button(label="Select Resource Pack", callback=lambda: dpg.show_item("rp_file_dialog_id"))
        dpg.add_text("Selected: none", tag="rp_selected_text", wrap=750)

    dpg.add_spacing(height=15) # Add extra space between groups

    # Song Details Group
    with dpg.group(horizontal=False, horizontal_spacing=10):
        dpg.add_separator()
        dpg.add_text("Step 3: Select Song Name and File", color=(50, 205, 50))
        
        # Song Name Input
        global input_song_name
        input_song_name = dpg.add_input_text(label="Enter Unique **Song Name**", source="string_value", width=300)

        # Song File
        dpg.add_button(label="Select Song (.ogg)", callback=lambda: dpg.show_item("song_dialog_id"))
        dpg.add_text("Selected: none", tag="song_selected_text", wrap=750)
    
    dpg.add_spacing(height=15) # Add extra space between groups

    # Options and Start Group
    with dpg.group(horizontal=False, horizontal_spacing=10):
        dpg.add_separator()
        dpg.add_text("Step 4: Options & Start", color=(138, 43, 226))
        
        # Checkbox
        dpg.add_checkbox(label="Add to Creeper Loot Table (Disc drops from Creepers)", callback=checkbox_callback, default_value=True)
        
        # Start Button
        dpg.add_button(label="START PROCESS", callback=start_callback, width=200, height=40)

dpg.create_viewport(title='Custom Title', width=1000, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()