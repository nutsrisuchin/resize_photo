import streamlit as st
from PIL import Image
import io

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
    for uploaded_image in uploaded_images:
        st.write(f"**Processing: {uploaded_image.name}**")
        try:
            st.image(uploaded_image, caption="Uploaded Image.", use_column_width=True)
            resized_img = resize_image(uploaded_image)
            
            if resized_img:
                img_buffer = io.BytesIO()
                resized_img.save(img_buffer, format="JPEG")
                img_bytes = img_buffer.getvalue()
                
                st.image(resized_img, caption="Resized Image.", use_column_width=True)
                st.download_button(
                    label="Download Resized Image",
                    data=img_bytes,
                    file_name=f"resized_{uploaded_image.name}",
                    mime="image/jpeg"
                )
        except Exception as e:
            st.error(f"Error displaying or downloading image: {e}")


