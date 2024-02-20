import streamlit as st
import cv2
import numpy as np
from PIL import Image
import pytesseract

def analyze_image(image):
    # Use Tesseract to extract word boxes and text
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    boxes_data = pytesseract.image_to_boxes(rgb_image)
    extracted_text = pytesseract.image_to_string(rgb_image)

    # Convert the image to grayscale for style analysis
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply edge detection
    edges = cv2.Canny(gray_image, 50, 150)

    # Find contours in the edge-detected image
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Analyze contours to infer style information for each letter
    letter_styles = []

    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        # Use bounding box information to infer style (e.g., bold or italic)
        aspect_ratio = w / h
        if aspect_ratio > 1.5:
            style = "Bold"
        elif aspect_ratio < 0.5:
            style = "Italic"
        else:
            style = "Regular"

        # Append style for each letter in the contour
        for letter_x in range(x, x + w):
            letter_styles.append(style)

    return extracted_text, letter_styles

def main():
    st.title("Image Analysis App")

    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        if st.button("Analyze Image"):
            # Convert PIL Image to OpenCV format
            image_cv = np.array(image)
            
            # Analyze the image and get results
            text_result, style_result = analyze_image(image_cv)

            # Display results
            st.subheader("Output 1: Extracted Text")
            st.text(text_result)

            st.subheader("Output 2: Style Analysis")
            for i, style in enumerate(style_result):
                st.text(f"Letter {i+1}: Style - {style}")

if __name__ == "__main__":
    main()
