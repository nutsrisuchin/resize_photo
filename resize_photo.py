import streamlit as st
from PIL import Image
import io
import zipfile

def resize_image(uploaded_image, target_resolution=(1920, 1080)):
    try:
        img = Image.open(uploaded_image)
        img_resized = img.resize(target_resolution, Image.ANTIALIAS)
        return img_resized
    except Exception as e:
        st.error(f"Error processing image: {e}")
        return None

st.title("Image Resizer to 1920x1080")

uploaded_images = st.file_uploader("Upload images", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

if uploaded_images:
    # Create an in-memory bytes buffer for the zip file
    zip_buffer = io.BytesIO()

    # Create a zip file to store resized images
    with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as zf:
        for uploaded_image in uploaded_images:
            st.write(f"**Processing: {uploaded_image.name}**")
            try:
                st.image(uploaded_image, caption="Uploaded Image.", use_column_width=True)
                resized_img = resize_image(uploaded_image)

                if resized_img:
                    # Save the resized image into the zip file
                    img_buffer = io.BytesIO()
                    resized_img.save(img_buffer, format="JPEG")
                    img_bytes = img_buffer.getvalue()
                    zf.writestr(f"resized_{uploaded_image.name}", img_bytes)
                    
                    st.image(resized_img, caption="Resized Image.", use_column_width=True)

            except Exception as e:
                st.error(f"Error processing image: {e}")

    # Provide a download button for the zip file
    st.write("Download all resized images in a ZIP file:")
    zip_buffer.seek(0)  # Reset buffer position
    st.download_button(
        label="Download ZIP",
        data=zip_buffer.getvalue(),
        file_name="resized_images.zip",
        mime="application/zip"
    )



