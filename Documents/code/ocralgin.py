import cv2
import pytesseract
import numpy as np
import os

def adjust_orientation(input_image_path, output_image_path):
    """
    Adjusts the orientation of an image containing handwritten text using Tesseract OCR.
    Handles rotation angles of 0, 90, 180, and 270 degrees.
    Resizes the image to maintain aspect ratio and saves the result.

    Args:
        input_image_path (str): Path to the input image file.
        output_image_path (str): Path to save the processed image file.
    """
    try:
        # 1. Load and Validate Image
        image = cv2.imread(input_image_path)
        if image is None:
            raise FileNotFoundError(f"Error: Could not open or find image file: {input_image_path}")

        # 2. Preprocess for OCR (Grayscale, Blur, Adaptive Thresholding)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)
        binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        
        # 3. Detect Text Orientation with Tesseract - Retry with different configs
        rotation_angle = 0
        orientation_script="N/A"
        try:
            # First attempt - default config
            osd = pytesseract.image_to_osd(binary, output_type=pytesseract.Output.DICT)
            rotation_angle = int(osd.get("rotate", 0))
            orientation_script=osd.get("script", "N/A")
        
        except pytesseract.TesseractNotFoundError:
           raise Exception("Error: Tesseract is not installed or not in PATH. Please make sure it's correctly configured.")

        except Exception as e:
           print(f"Warning: Could not detect orientation using default config. Trying alternative config. Error : {str(e)}")
           
           #Second Attempt with different configuration
           try:
             osd = pytesseract.image_to_osd(binary, output_type=pytesseract.Output.DICT,config='--psm 0')
             rotation_angle = int(osd.get("rotate", 0))
             orientation_script=osd.get("script", "N/A")
           
           except Exception as e2:
            print(f"Warning: Could not detect orientation using alternative config also. Proceeding with the original image. Error:{str(e2)}")
            rotation_angle = 0 #Proceed with original image if error
            orientation_script = "N/A"

        print(f"Detected rotation angle: {rotation_angle} degrees, Script: {orientation_script}")

       # 4. Rotate Image based on Angle
        if rotation_angle == 180:
            rotation_flag = cv2.ROTATE_180
        elif rotation_angle == 90:
            rotation_flag = cv2.ROTATE_90_COUNTERCLOCKWISE
        elif rotation_angle == 270:
            rotation_flag = cv2.ROTATE_90_CLOCKWISE
        else:
            rotation_flag = None


        # Rotate the image only if a rotation_flag is set
        if rotation_flag is not None:
            corrected_image = cv2.rotate(image, rotation_flag)
        else:
          corrected_image = image
        
        # 5. Resize Image (Maintain Aspect Ratio)
        height, width = corrected_image.shape[:2]
        max_dim = 1000  # Maximum dimension for resizing
        scale = min(max_dim / width, max_dim / height)
        new_width = int(width * scale)
        new_height = int(height * scale)
        resized_image = cv2.resize(corrected_image, (new_width, new_height), interpolation=cv2.INTER_AREA)

        # 6. Save the Processed Image
        cv2.imwrite(output_image_path, resized_image)
        print(f"Image processed and saved to: {output_image_path}")

    except FileNotFoundError as e:
         print(f"Error: {str(e)}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    # Example Usage
    input_image_path = "input_image.jpg"  # Replace with your input file path
    output_image_path = "output_image.jpg"  # Replace with your output file path

    # Check if the input file exists
    if not os.path.exists(input_image_path):
        print(f"Error: Input image not found at {input_image_path}. Please provide a valid image file path.")
    else:
        adjust_orientation(input_image_path, output_image_path)