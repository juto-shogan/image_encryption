# image_encryption

# Selective ROI Image Encryption System

This project implements a **Region of Interest (ROI) Image Encryption** system using a  **Chaotic Logistic Map** . It allows users to encrypt specific parts of a medical image (ROI) while leaving the rest of the image untouched. This is particularly useful for medical imaging where patient privacy (ROI) is critical, but the surrounding context must remain visible.

## Features

* **Selective Encryption:** Encrypt only the sensitive part of an image (ROI).
* **Chaotic Logistic Map:** Uses a mathematical chaotic map to generate pseudo-random encryption keys, sensitive to initial conditions (**$r$** and **$x_0$**).
* **Two Modes of Operation:**
  * **Automatic:** Automatically detects the area with the highest details (variance).
  * **Manual:** Allows the user to select the specific region to encrypt.
* **Dual Interface:**
  * **Desktop Script (`main.py`):** Draw the ROI directly on the image with your mouse.
  * **Web App (`app.py`):** User-friendly web interface with sliders for ROI adjustment.
* **Format Handling:** Supports `.jpg`, `.png`, and `.jfif` uploads, and saves all encrypted output as `.png` to prevent data loss.

---

## Project Structure

**Plaintext**

```
Project/
│
├── crypto_logic.py    # CORE LOGIC: Contains math, encryption, and ROI functions.
├── main.py            # SCRIPT: Run this for the desktop version (draw with mouse).
├── app.py             # WEB APP: Run this for the browser version (sliders).
└── images/            # Folder where you can store input images (optional).
    └── encrypted/     # The system automatically creates this folder for outputs.
```

---

## Installation & Setup

1. **Install Python:** Ensure you have Python installed on your system.
2. **Install Dependencies:** Open your terminal or command prompt and run the following command to install the required libraries:

**Bash**

```
pip install streamlit opencv-python numpy pillow
```

---

## Usage

### Option 1: The Web Interface (Recommended)

This version allows you to use sliders to pick your ROI and see a live preview.

1. Open your terminal in the project folder.
2. Run the app:
   **Bash**

   ```
   streamlit run app.py
   ```
3. A browser window will open (usually at `http://localhost:8501`).
4. **Steps:**

   * Select "Manual ROI" in the sidebar.
   * Upload your image (supports `.jfif`, `.jpg`, `.png`).
   * Adjust the sliders to move the **Red Box** over the area you want to hide.
   * Click  **Encrypt & Save ROI** .
   * The encrypted image is saved to the `encrypted/` folder.

### Option 2: The Desktop Script

This version allows you to draw the box directly on the image.

1. Open your terminal.
2. Run the script:
   **Bash**

   ```
   python main.py
   ```
3. **Steps:**

   * Choose option `2` for Manual Mode.
   * A window will pop up showing your image.
   * **Click and Drag** your mouse to draw a box.
   * Press **ENTER** to confirm (or `c` to cancel).
   * The script will encrypt the selection and save it.

---

## Important Note on File Formats

* **Input:** The system accepts `.jpg`, `.jpeg`, `.png`, and `.jfif`.
* **Output:** All encrypted images are forcefully saved as  **`.png`** .
  * **Why?** JPEG/JFIF formats use compression that alters pixel values slightly. If a single pixel value changes, the chaotic decryption will fail. PNG is "lossless," ensuring the data remains exact for decryption.

---

## Security Parameters

* **$r$ (Growth Rate):** Controls the chaotic behavior. The system uses a default near **$3.99$** for maximum chaos.
* **$x_0$ (Initial Condition):** The starting point of the map (0 to 1). Acts as part of the "password." Both the sender and receiver need the exact same **$r$** and **$x_0$** values to decrypt the image.
