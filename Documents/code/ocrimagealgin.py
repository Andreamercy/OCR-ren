import cv2
import numpy as np
import pytesseract
import os

def correct_image_orientation(input_path, output_path):
    """
    Corrects the orientation of an image containing handwritten text.

    Args:
        input_path: Path to the input image file.
        output_path: Path to save the corrected image.

    Raises:
        FileNotFoundError: If the input file does not exist.
        RuntimeError: If Tesseract OCR is not installed or configured correctly.
        ValueError: If the image is not readable or doesn't contain recognizable text.
    """

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    try:
        img = cv2.imread(input_path, cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise ValueError("Could not read the image. Check if the file is a valid image format.")

        # Preprocessing (improve OCR accuracy)
        _, img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        kernel = np.ones((2, 2), np.uint8)  # Adjust kernel size as needed
        img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

        # Use Tesseract to detect text orientation
        details = pytesseract.image_to_osd(img)
        rotation_angle = int(details.split('\n')[2].split(': ')[1])

        if rotation_angle == 0:
            print("Image is correctly oriented.")
        elif rotation_angle == 180:
            print("Rotating image 180 degrees.")
            img = cv2.rotate(img, cv2.ROTATE_180)
        elif rotation_angle == 90:
            print("Rotating image 270 degrees.")
            img = cv2.rotate(img, cv2.ROTATE_270)
        elif rotation_angle == 270:
            print("Rotating image 90 degrees.")
            img = cv2.rotate(img,90)
        else:
            print(f"Detected unusual rotation: {rotation_angle}. No rotation applied.")

        # Maintain aspect ratio while resizing if needed.
        max_width = 800 # Set your desired max width
        max_height = 600 # Set your desired max height
        h, w = img.shape[:2]
        if w > max_width or h > max_height:
          if w > h:
            new_w = max_width
            new_h = int(h * (new_w / w))
          else:
            new_h = max_height
            new_w = int(w * (new_h / h))
          img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

        cv2.imwrite(output_path, img)
        print(f"Corrected image saved to: {output_path}")

    except pytesseract.TesseractNotFoundError:
        raise RuntimeError("Tesseract is not installed. Please install Tesseract OCR.")
    except ValueError as ve:
      raise ve
    except Exception as e:
        print(f"An unexpected error occurred: {e}")



# Example usage:
input_image_path = "input.png"  # Replace with your input image path
output_image_path = "output.png" # Replace with your desired output path

try:
    correct_image_orientation(input_image_path, output_image_path)
except (FileNotFoundError, RuntimeError, ValueError) as e:
    print(f"Error: {e}")