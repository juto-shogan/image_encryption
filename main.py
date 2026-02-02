import cv2
import crypto_logic as cl  # Importing our logic file

def main():
    image_path = "medical_scan.jpg"  # CHANGE THIS to your image file
    
    # 1. Load Image
    img = cv2.imread(image_path, 0) # Load as grayscale
    if img is None:
        print(f"Error: Could not find {image_path}")
        return

    print("--- Medical Image Encryption System ---")
    print("1. Automatic ROI (Variance based)")
    print("2. Manual ROI (Draw with mouse)")
    choice = input("Select Mode (1 or 2): ")

    # 2. Select ROI
    if choice == "1":
        roi = cl.automatic_roi(img)
        print(f"Automatic ROI found: {roi}")
    else:
        print("Draw a rectangle and press ENTER. Press 'c' to cancel.")
        # Opens a window to draw the box
        x, y, w, h = cv2.selectROI("Select ROI", img, showCrosshair=True)
        roi = (x, y, w, h)
        cv2.destroyAllWindows()
        if w == 0 or h == 0:
            print("No ROI selected. Exiting.")
            return

    # 3. Encryption Parameters
    r_val = 3.99
    x0_val = 0.5

    # 4. Encrypt
    encrypted_img = cl.process_image(img, roi, r_val, x0_val)
    
    # 5. Save
    save_name = "encrypted_" + image_path
    saved_path = cl.save_encrypted_file(encrypted_img, save_name)
    print(f"✅ Encrypted image saved to: {saved_path}")

    # 6. Verify Decryption (Optional proof it works)
    decrypted_img = cl.process_image(encrypted_img, roi, r_val, x0_val)
    cv2.imshow("Encrypted", encrypted_img)
    cv2.imshow("Decrypted (Proof)", decrypted_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()