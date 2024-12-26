'''
import cv2
import numpy as np
from pytesseract import pytesseract, Output

def correct_card_orientation(image, max_dim=1000):
    """
    Check and correct the orientation of the history card based on text alignment.
    Resizes the image while maintaining the aspect ratio.

    Args:
        image (numpy array): Input image of the history card.
        max_dim (int): Maximum dimension for resizing.

    Returns:
        aligned_image (numpy array): Image with corrected orientation and size.
        rotation_angle (float): Angle by which the image was rotated.
    """
    def get_ocr_confidence(img):
        """Extract text using OCR and calculate the confidence."""
        ocr_data = pytesseract.image_to_data(img, output_type=Output.DICT)
        confidences = [int(conf) for conf in map(str, ocr_data['conf']) if conf.isdigit()]
        return np.mean(confidences) if confidences else 0

    def rotate_image(img, angle):
        """Rotate the image by a specific angle while preserving dimensions."""
        (h, w) = img.shape[:2]
        center = (w // 2, h // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(img, rotation_matrix, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return rotated

    best_angle = 0
    best_confidence = 0
    aligned_image = image.copy()  # Start with a copy to avoid modifying original
    
    # Preprocess image for OCR
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    _, preprocessed = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Try rotating the image by 0, 90, 180, and 270 degrees
    for angle in [0, 90, 180, 270]:
        rotated = rotate_image(image, angle)  # Rotate original image

        # Calculate OCR confidence
        confidence = get_ocr_confidence(preprocessed if angle == 0 else rotated)

        # Update the best orientation
        if confidence > best_confidence:
            best_confidence = confidence
            best_angle = angle
            aligned_image = rotated.copy()  # Update the aligned image

    # Handle resizing for correct output dimensions (if rotation is 90 or 270)
    if best_angle == 90 or best_angle == 270:
        aligned_image = cv2.resize(aligned_image, (image.shape[1], image.shape[0]))  # Swap dimensions for 90/270

    # Resize to maintain aspect ratio and apply max_dim limit
    height, width = aligned_image.shape[:2]
    scale = min(max_dim / width, max_dim / height)
    new_width = int(width * scale)
    new_height = int(height * scale)
    resized_image = cv2.resize(aligned_image, (new_width, new_height), interpolation=cv2.INTER_AREA)

    return resized_image, best_angle

# Example usage
if __name__ == "__main__":
    # Load the image
    input_image = cv2.imread("input_image.jpg")
    if input_image is None:
        print("Error: Could not read the file. Check the file path or name.")
        exit(1)

    # Correct the orientation
    corrected_image, angle = correct_card_orientation(input_image, max_dim=1000)

    # Save the output image
    output_filename = "corrected_history_card.jpg"
    cv2.imwrite(output_filename, corrected_image)
    print(f"Corrected image saved as {output_filename}")

    # Display the result
    print(f"Image rotated by {angle} degrees.")
    cv2.imshow("Corrected Image", corrected_image)


     
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
'''

import cv2
import numpy as np
from pytesseract import pytesseract, Output

def correct_card_orientation(image, max_dim=1000):
    """
    Check and correct the orientation of the history card based on text alignment.
    Resizes the image while maintaining the aspect ratio.

    Args:
        image (numpy array): Input image of the history card.
        max_dim (int): Maximum dimension for resizing.

    Returns:
        aligned_image (numpy array): Image with corrected orientation and size.
        rotation_angle (float): Angle by which the image was rotated.
    """
    def get_ocr_confidence(img):
        """Extract text using OCR and calculate the confidence."""
        ocr_data = pytesseract.image_to_data(img, output_type=Output.DICT)
        confidences = [int(conf) for conf in map(str, ocr_data['conf']) if conf.isdigit()]
        return np.mean(confidences) if confidences else 0

    def rotate_image(img, angle):
        """Rotate the image by a specific angle without preserving dimensions."""
        (h, w) = img.shape[:2]
        center = (w // 2, h // 2)
        rotation_matrix = cv2.getRotationMatrix2D(center, angle, 1.0)

        # Calculate new bounding box size after rotation
        abs_cos = abs(rotation_matrix[0, 0])
        abs_sin = abs(rotation_matrix[0, 1])
        new_w = int(h * abs_sin + w * abs_cos)
        new_h = int(h * abs_cos + w * abs_sin)

        # Adjust the rotation matrix to keep the image centered
        rotation_matrix[0, 2] += (new_w / 2) - center[0]
        rotation_matrix[1, 2] += (new_h / 2) - center[1]

        # Perform the rotation
        rotated = cv2.warpAffine(img, rotation_matrix, (new_w, new_h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return rotated

    best_angle = 0
    best_confidence = 0
    aligned_image = image.copy()  # Start with a copy to avoid modifying original
    
    # Preprocess image for OCR
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    _, preprocessed = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Try rotating the image by 0, 90, 180, and 270 degrees
    for angle in [0, 90, 180, 270]:
        rotated = rotate_image(image, angle)  # Rotate original image

        # Calculate OCR confidence
        confidence = get_ocr_confidence(preprocessed if angle == 0 else rotated)

        # Update the best orientation
        if confidence > best_confidence:
            best_confidence = confidence
            best_angle = angle
            aligned_image = rotated.copy()  # Update the aligned image

    # Resize to maintain aspect ratio and apply max_dim limit
    height, width = aligned_image.shape[:2]
    scale = min(max_dim / width, max_dim / height)
    new_width = int(width * scale)
    new_height = int(height * scale)
    resized_image = cv2.resize(aligned_image, (new_width, new_height), interpolation=cv2.INTER_AREA)

    return resized_image, best_angle

# Example usage
if __name__ == "__main__":
    # Load the image
    input_image = cv2.imread("input_image.jpg")
    if input_image is None:
        print("Error: Could not read the file. Check the file path or name.")
        exit(1)

    # Correct the orientation
    corrected_image, angle = correct_card_orientation(input_image, max_dim=1000)

    # Save the output image
    output_filename = "corrected_history_card.jpg"
    cv2.imwrite(output_filename, corrected_image)
    print(f"Corrected image saved as {output_filename}")

    # Display the result
    print(f"Image rotated by {angle} degrees.")
    cv2.imshow("Corrected Image", corrected_image)

