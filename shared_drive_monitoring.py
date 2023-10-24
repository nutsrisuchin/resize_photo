import streamlit as st
import json
import os
import psutil
import pandas as pd
import numpy as np

# ... [Previous utility functions]

# Additional function to visualize drive space
def visualize_drive_space(drive, drive_info):
    df = pd.DataFrame({
        'Space': ['Used', 'Free'],
        'GB': [drive_info['used'] / (1024**3), drive_info['free'] / (1024**3)]
    })
    st.bar_chart(df.set_index('Space'))

# ... [display_folder_data function]

def app():
    st.title("Shared Drive Space Monitoring")
    
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
        
        # Pie chart for top-level folder distribution
        folder_sizes = [f['size'] for f in drive_data['subfolders']]
        folder_names = [f['name'] for f in drive_data['subfolders']]
        st.pie_chart(pd.Series(folder_sizes, index=folder_names))
        
        st.write("\n")
        st.write("### Subfolder Sizes")
        display_folder_data(drive_data["subfolders"])

    # Assuming you have historical data stored in a CSV
    if os.path.exists("historical_data.csv"):
        df = pd.read_csv("historical_data.csv")
        st.write("### Drive Usage Trend")
        st.line_chart(df.set_index('Date'))

# ... [App Execution]

if __name__ == "__main__":
    app()

