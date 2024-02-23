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
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Use Tesseract to extract word boxes and text
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

    final_output = []

    # Iterate through each word box and extract color, style, and position for each word
    for box_data in boxes_data.splitlines():
        box = box_data.split()
        x, y, w, h = int(box[1]), int(box[2]), int(box[3]), int(box[4])
        word_image = rgb_image[y:h, x:w]
        average_word_color = np.mean(word_image, axis=(0, 1)).astype(int)
        word = box_data[0]
        mini_output = []
        #Print each letter, its color, style, and position
        print("Letter:", word)
        print("Position: x1 = {}, y1 = {}, x2 = {}, y2 = {}".format(x, y, w, h))
        #mini_output.append(word)
        #mini_output.append("Position :  x1, y1, x2, y2 :")
        #mini_output.append([x, y, w, h])
        # Extract style for each letter in the word
        for i, letter in enumerate(word):
            letter_style = letter_styles[x + i]  # Assuming x is the starting x-coordinate of the word
            print(f"    Letter: {letter}, Color: {tuple(average_word_color)}, Style: {letter_style}")
            mini_output.append("Letter : ")
            mini_output.append(letter)
            
            mini_output.append(tuple(average_word_color))
            mini_output.append("Letter Style :")
            mini_output.append(letter_style)
        final_output.append(mini_output)
        print("\n")
    return final_output

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
