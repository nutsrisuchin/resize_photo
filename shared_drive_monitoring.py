import streamlit as st
import json
import os
import psutil
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def get_file_type_sizes(path):
    """Get sizes of files grouped by their extensions"""
    file_sizes = {}
    for foldername, subfolders, filenames in os.walk(path):
        for filename in filenames:
            _, ext = os.path.splitext(filename)
            ext = ext[1:].upper()  # Remove dot and make uppercase
            filepath = os.path.join(foldername, filename)
            if os.path.exists(filepath):  # Check if file exists
                file_size = os.path.getsize(filepath)
                file_sizes[ext] = file_sizes.get(ext, 0) + file_size

    return sorted(file_sizes.items(), key=lambda x: x[1], reverse=True)

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

def display_folder_data(folders, level=1):
    """
    Display folder data recursively.
    """
    for folder in folders:
        st.write(f"{'  ' * level}Folder: {folder['name']}, Size: {convert_bytes_to_readable(folder['size'])}")
        if level < 2:  # If you want to increase the depth, modify this value
            display_folder_data(folder['subfolders'], level + 1)


def visualize_subfolder_comparison(subfolders):
    # [NOTE: Modified to show only 1 level]
    folder_sizes = [f['size'] for f in subfolders if 'subfolders' not in f]
    folder_names = [f['name'] for f in subfolders if 'subfolders' not in f]

    df = pd.DataFrame({
        'Folder': folder_names,
        'Size (GB)': [size / (1024**3) for size in folder_sizes]
    })

    fig, ax = plt.subplots(figsize=(12, 6))
    df.sort_values('Size (GB)', ascending=True).plot(kind='barh', x='Folder', y='Size (GB)', ax=ax)
    plt.title('Subfolder Size Comparison')
    plt.tight_layout()
    st.pyplot(fig)

def app():
    st.title("Shared Drive Space Monitoring")
    
    # Load data from JSON file
    with open("drive_data.json", "r") as f:
        data = json.load(f)

    # Assuming you're only working with a single drive in this example
    drive, drive_data = list(data.items())[0]
    st.write(f"## Drive: {drive}")

    subfolder_names = [f['name'] for f in drive_data['subfolders']]
    selected_subfolder = st.selectbox("Choose a subfolder to explore:", ["-"] + subfolder_names)

    # Display drive details and chart
    visualize_drive_space(drive, drive_data["drive_info"])
    drive_info = drive_data["drive_info"]
    st.write(f"📁 Total Space: {drive_info['total'] / (1024**3):.2f} GB")
    st.write(f"Used Space: {drive_info['used'] / (1024**3):.2f} GB")
    st.write(f"Free Space: {drive_info['free'] / (1024**3):.2f} GB")
    st.write(f"Percent Used: {drive_info['percent_used']}%")

    # If a subfolder is selected, show its details
    if selected_subfolder != "-":
        for sf in drive_data['subfolders']:
            if sf['name'] == selected_subfolder:
                # Visualize subfolder comparison
                visualize_subfolder_comparison([sf])
                
                # Display file type sizes in table
                path = os.path.join(drive, selected_subfolder)
                file_types_sizes = get_file_type_sizes(path)
                file_types_df = pd.DataFrame(file_types_sizes, columns=['File Type', 'Size (bytes)'])
                st.table(file_types_df)

if __name__ == "__main__":
    app()
