import streamlit as st
import json
import os
import psutil
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ... [Previous utility functions]

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

# Visualization function for subfolder comparison
def visualize_subfolder_comparison(subfolders):
    folder_sizes = [f['size'] for f in subfolders]
    folder_names = [f['name'] for f in subfolders]

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
    
    # Sidebar option to show subfolders
    show_subfolders = st.sidebar.checkbox("Show Subfolder Details", True)

    # Load data from JSON file
    with open("drive_data.json", "r") as f:
        data = json.load(f)

    for drive, drive_data in data.items():
        st.write(f"## Drive: {drive}")
        
        # Bar chart visualization for drive space
        visualize_drive_space(drive, drive_data["drive_info"])
        
        drive_info = drive_data["drive_info"]
        st.write(f"📁 Total Space: {drive_info['total'] / (1024**3):.2f} GB")
        st.write(f"Used Space: {drive_info['used'] / (1024**3):.2f} GB")
        st.write(f"Free Space: {drive_info['free'] / (1024**3):.2f} GB")
        st.write(f"Percent Used: {drive_info['percent_used']}%")
        
        # Visualization for subfolder comparison
        visualize_subfolder_comparison(drive_data["subfolders"])
        
        if show_subfolders:
            st.write("\n")
            st.write("### Subfolder Sizes")
            display_folder_data(drive_data["subfolders"])

# ... [App Execution]

if __name__ == "__main__":
    app()


