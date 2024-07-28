import streamlit as st
import pandas as pd
import numpy as np
import cv2

from module1 import func


st.title('Race Smart v2.0')

uploaded_file = st.file_uploader("Choose a file", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Convert the file to an OpenCV image
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    image = cv2.imdecode(file_bytes, 1)
    
    # Save the image using OpenCV
    cv2.imwrite("working_image.png", image)
    
    # Display the image in Streamlit
    st.image(image, channels="BGR", caption="Uploaded Image")
    feedback_text = func("working_image.png")

    st.image("Posture_Analysis.jpg", channels="BGR", caption="Uploaded Image")
    st.text(feedback_text)
