import os
import json
import streamlit as st
import pandas as pd


# Visualization Functions
def display_folder_data(folders, level=1):
    """
    Display folder data recursively.
    """
    for folder in folders:
        st.write(f"{'  ' * level}Folder: {folder['name']}, Size: {convert_bytes_to_readable(folder['size'])}")
        if level < 2:  # If you want to increase the depth, modify this value
            display_folder_data(folder['subfolders'], level + 1)

def visualize_drive_space(drive, drive_info):
    df = pd.DataFrame({
        'Space': ['Used', 'Free'],
        'GB': [drive_info['used'] / (1024**3), drive_info['free'] / (1024**3)]
    })
    
    fig, ax = plt.subplots()
    df.set_index('Space').plot(kind='bar', ax=ax, legend=False)
    plt.title(f"Drive: {drive} Usage")
    plt.ylabel("Size (GB)")
    plt.xticks(rotation=0)
    st.pyplot(fig)

def visualize_file_type_sizes(file_types):
    file_type_df = pd.DataFrame(list(file_types.items()), columns=['File Type', 'Size (MB)'])
    st.table(file_type_df.sort_values('Size (MB)', ascending=False))

# Extract data
shared_drives = ["N:\\T-II\\99 Public\\"]
data = {}

for drive in shared_drives:
    data[drive] = {
        "drive_info": get_drive_space(drive),
        "subfolders": get_subfolder_sizes(drive),
        "file_types": get_file_type_sizes(drive)
    }

# Streamlit Visualization
st.title("Shared Drive Monitoring")

selected_drive = st.selectbox("Select a drive to monitor", list(data.keys()))
drive_data = data[selected_drive]

visualize_drive_space(selected_drive, drive_data["drive_info"])

st.write("## File Type Statistics at Top Level")
visualize_file_type_sizes(drive_data["file_types"])

st.write("## Subfolder Data")
display_folder_data(drive_data["subfolders"])

# Extract file type data for subfolders
all_file_types = {}
for folder in drive_data["subfolders"]:
    for f_type, f_size in folder["file_types"].items():
        all_file_types[f_type] = all_file_types.get(f_type, 0) + f_size

st.write("## File Type Statistics for Subfolders")
visualize_file_type_sizes(all_file_types)
