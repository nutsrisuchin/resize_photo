import streamlit as st
import json

def app():
    st.title("Shared Drive Space Monitoring")
    
    # Load data from JSON file
    with open("drive_data.json", "r") as f:
        data = json.load(f)

    for drive, drive_data in data.items():
        st.write(f"## Drive: {drive}")
        drive_info = drive_data["drive_info"]
        
        st.write(f"📁 Total Space: {drive_info['total'] / (1024**3):.2f} GB")
        st.write(f"Used Space: {drive_info['used'] / (1024**3):.2f} GB")
        st.write(f"Free Space: {drive_info['free'] / (1024**3):.2f} GB")
        st.write(f"Percent Used: {drive_info['percent_used']}%")
        
        st.write("\n")
        st.write("### Subfolder Sizes")
        display_folder_data(drive_data["subfolders"])

if __name__ == "__main__":
    app()
