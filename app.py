import streamlit as st
import numpy as np
import cv2
from PIL import Image
import crypto_logic as cl  # Ensure crypto_logic.py is in the same folder

st.set_page_config(page_title="Medical Crypto App", layout="wide")
st.title("🔐 Selective ROI Image Encryption")

# =========================================================
# SIDEBAR SETTINGS
# =========================================================
st.sidebar.header("1. Settings")
mode = st.sidebar.radio("Selection Mode", ["Automatic ROI", "Manual ROI"])

st.sidebar.header("2. Security Keys")
r = st.sidebar.slider("Logistic Parameter (r)", 3.70, 4.00, 3.99)
x0 = st.sidebar.slider("Initial Condition (x0)", 0.01, 0.99, 0.50)

# =========================================================
# FILE UPLOAD
# =========================================================
# Fix 1: Added 'jfif' to the allowed types
uploaded_file = st.file_uploader("Upload Medical Image (Grayscale)", type=['png', 'jpg', 'jpeg', 'jfif'])

if uploaded_file:
    # Convert file to OpenCV format
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_GRAYSCALE)

    # Fix 2: Check if image loaded correctly
    if img is None:
        st.error("Error: Could not load the image. Please try a different file.")
        st.stop()

    h, w = img.shape
    roi = (0, 0, 0, 0)

    # =========================================================
    # ROI SELECTION LOGIC
    # =========================================================
    if mode == "Automatic ROI":
        roi = cl.automatic_roi(img)
        st.info(f"✅ Auto-detected ROI (Variance based): {roi}")

    else:  # MANUAL MODE
        st.sidebar.header("3. Manual ROI Controls")
        st.sidebar.info("Adjust sliders to move the RED box.")

        # X and Y Start Positions
        x_start = st.sidebar.slider("X Position (Horizontal)", 0, w - 10, 50)
        y_start = st.sidebar.slider("Y Position (Vertical)", 0, h - 10, 50)

        # Dynamic Max Width/Height to prevent going out of bounds
        max_width = w - x_start
        max_height = h - y_start

        roi_w = st.sidebar.slider("Box Width", 10, max_width, min(100, max_width))
        roi_h = st.sidebar.slider("Box Height", 10, max_height, min(100, max_height))

        roi = (x_start, y_start, roi_w, roi_h)

    # =========================================================
    # PREVIEW (LIVE FEEDBACK)
    # =========================================================
    # Convert to color just for the preview (so we can draw a red box)
    preview_img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
    px, py, pw, ph = roi
    
    # Draw the Red Rectangle
    cv2.rectangle(preview_img, (px, py), (px + pw, py + ph), (255, 0, 0), 3)

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Original Image + ROI Preview")
        st.image(preview_img, use_container_width=True)

    # =========================================================
    # ENCRYPTION ACTION
    # =========================================================
    if st.button("Encrypt & Save ROI"):
        with st.spinner("Encrypting..."):
            # 1. Encrypt using logic file
            encrypted_img = cl.process_image(img, roi, r, x0)

            # Fix 3: Force .png extension to prevent data corruption
            # Removes old extension and adds .png
            original_name = uploaded_file.name.rsplit('.', 1)[0]
            save_name = f"enc_{original_name}.png"
            
            # 2. Save
            saved_path = cl.save_encrypted_file(encrypted_img, save_name)

            # 3. Display Result
            with col2:
                st.subheader("Encrypted Result")
                st.image(encrypted_img, use_container_width=True)
                st.success(f"Image saved locally to: {saved_path}")

            # 4. Decryption Proof (Verification)
            decrypted_check = cl.process_image(encrypted_img, roi, r, x0)
            
            # Show small proof below
            st.write("---")
            st.caption("Decryption Verification (Internal Check):")
            st.image(decrypted_check, width=200, clamp=True)