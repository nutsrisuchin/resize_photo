import os
import json
import streamlit as st
import pandas as pd

# Conversion Functions
def bytes_to_mb(size_in_bytes):
    return size_in_bytes / (2**20)  # Convert bytes to megabytes

# Visualization Functions
def display_folder_data(folders, level=1):
    # Ensure sizes are converted to MB for display
    for folder in folders:
        folder_size = bytes_to_mb(folder["size"])
        st.write(f"{'--' * level} {folder['name']} - {folder_size:.2f} MB")
        if "subfolders" in folder:
            display_folder_data(folder["subfolders"], level + 1)

def visualize_drive_space(drive, drive_info):
    # Convert drive info sizes to MB for display
    total_mb = bytes_to_mb(drive_info["total"])
    used_mb = bytes_to_mb(drive_info["used"])
    free_mb = bytes_to_mb(drive_info["free"])
    
    st.write(f"Total space on {drive}: {total_mb:.2f} MB")
    st.write(f"Used space on {drive}: {used_mb:.2f} MB")
    st.write(f"Free space on {drive}: {free_mb:.2f} MB")

def visualize_file_type_sizes(file_types):
    file_type_data = {f_type: bytes_to_mb(f_size) for f_type, f_size in file_types.items()}
    file_type_df = pd.DataFrame(list(file_type_data.items()), columns=['File Type', 'Size (MB)'])
    st.table(file_type_df.sort_values('Size (MB)', ascending=False))

# Load extracted data from JSON
with open("drive_data.json", "r") as f:
    data = json.load(f)

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
