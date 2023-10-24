import streamlit as st
import json
import pandas as pd
import os

BYTES_IN_GB = 1e9  # 1 GB = 1e9 bytes

# Load data from JSON
with open("drive_data.json", "r") as f:
    data = json.load(f)

# Streamlit app
def app():
    # Allow user to select the drive/folder
    selected_drive = st.selectbox("Select drive/folder", list(data.keys()))
    drive_data = data[selected_drive]
    
    st.title(f"Data for {selected_drive}")
    
    # Display drive info
    st.subheader("Drive Info")
    st.write(f"Total space: {drive_data['drive_info']['total'] / BYTES_IN_GB:.2f} GB")
    st.write(f"Used space: {drive_data['drive_info']['used'] / BYTES_IN_GB:.2f} GB")
    st.write(f"Free space: {drive_data['drive_info']['free'] / BYTES_IN_GB:.2f} GB")

    # Allow user to specify subfolder to view
    subfolders = [sf["name"] for sf in drive_data["subfolders"]]
    selected_subfolder = st.selectbox("Select subfolder", ["-"] + subfolders)
    
    if selected_subfolder != "-":
        for sf in drive_data["subfolders"]:
            if sf["name"] == selected_subfolder:
                st.subheader(f"Data for {selected_subfolder}")
                st.write(f"Used space: {sf['size'] / BYTES_IN_GB:.2f} GB")
                # Table for file type sizes
                st.subheader("Space by File Type (in GB)")
                file_type_df = pd.DataFrame(sf["file_types"].items(), columns=["File Type", "Size"])
                file_type_df["Size"] = file_type_df["Size"] / BYTES_IN_GB
                st.table(file_type_df)
                break
    
    # Pie chart for space used by 1-level subfolders
    st.subheader("Space Distribution of 1-level Subfolders")
    folder_names = [sf["name"] for sf in drive_data["subfolders"]]
    folder_sizes = [sf["size"] for sf in drive_data["subfolders"]]
    st.pie_chart(pd.Series(folder_sizes, index=folder_names))

if __name__ == "__main__":
    app()

