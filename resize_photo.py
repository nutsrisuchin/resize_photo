import streamlit as st
from PIL import Image
import io
import zipfile

def resize_image(uploaded_image, target_width=1920):
    try:
        img = Image.open(uploaded_image)

        # Calculate the aspect ratio
        aspect_ratio = img.height / img.width
        new_height = int(target_width * aspect_ratio)

        img_resized = img.resize((target_width, new_height), Image.ANTIALIAS)
        return img_resized
    except Exception as e:
        st.error(f"Error processing image: {e}")
        return None

st.title("Image Resizer to 1920 Width")

uploaded_images = st.file_uploader("Upload images", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

if uploaded_images:
    # Counters for uploaded and resized images
    uploaded_count = len(uploaded_images)
    resized_count = 0
    
    # Create an in-memory bytes buffer for the zip file
    zip_buffer = io.BytesIO()

    # Create a zip file to store resized images
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as zf:
        for uploaded_image in uploaded_images:
            try:
                resized_img = resize_image(uploaded_image)

                if resized_img:
                    # Save the resized image into the zip file
                    img_buffer = io.BytesIO()
                    resized_img.save(img_buffer, format="JPEG")
                    img_bytes = img_buffer.getvalue()
                    zf.writestr(f"resized_{uploaded_image.name}", img_bytes)
                    
                    # Increment the counter for successfully resized images
                    resized_count += 1

            except Exception as e:
                st.error(f"Error processing image: {e}")

    st.write(f"**Number of uploaded images:** {uploaded_count}")
    st.write(f"**Number of successfully resized images:** {resized_count}")

    # Provide a download button for the zip file
    st.write("Download all resized images in a ZIP file:")
    zip_buffer.seek(0)  # Reset buffer position
    st.download_button(
        label="Download ZIP",
        data=zip_buffer.getvalue(),
        file_name="resized_images.zip",
        mime="application/zip"
    )

