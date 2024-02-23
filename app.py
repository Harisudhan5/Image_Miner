import streamlit as st
import cv2
import numpy as np
from PIL import Image
import pytesseract

def extract_text(image):
    # Use Tesseract to extract word boxes and text
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    extracted_text = pytesseract.image_to_string(rgb_image)
    return extracted_text

def analyze_style(image):
    # Convert the image to grayscale for style analysis
    
    

    return letter_styles

def main():
    
    st.title("Image Miner")

    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        if st.button("Mine the Image"):
            # Convert PIL Image to OpenCV format
            image_cv = np.array(image)

            # Output 1: Extracted Text
            text_result = extract_text(image_cv)
            st.subheader("Output 1: Extracted Text")
            st.text(text_result)

            # Output 2: Style Analysis
            style_result = analyze_style(image_cv)
            st.subheader("Output 2: Text Characteristics")
            for i, style in enumerate(style_result):
                st.text(f"Letter {i+1}: Style - {style}")

if __name__ == "__main__":
    main()
