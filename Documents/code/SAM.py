
'''
import cv2
from pytesseract import image_to_osd

def correct_orientation(image):
    """
    Correct the orientation of a handwritten history card to 0°, 90°, 180°, or 270°.

    Args:
        image (numpy array): Input handwritten history card image.

    Returns:
        aligned_image (numpy array): Image with corrected orientation.
        rotation_angle (int): Angle by which the image was rotated to align (0, 90, 180, 270).
    """
    # Detect orientation using Tesseract OSD
    osd = image_to_osd(image, output_type="dict")
    rotation_angle = osd.get("rotate", 0)

    # Rotate the image to the nearest 90-degree orientation
    if rotation_angle == 90:
        aligned_image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    elif rotation_angle == 180:
        aligned_image = cv2.rotate(image, cv2.ROTATE_180)
    elif rotation_angle == 270:
        aligned_image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    else:
        # No rotation needed
        aligned_image = image

    return aligned_image, rotation_angle


# Example usage
if __name__ == "__main__":
    # Load the handwritten history card image
    input_image = cv2.imread("input_image.jpg")  # Replace with your image file path

    if input_image is None:
        raise FileNotFoundError("The image file was not found. Please check the file path.")

    # Correct orientation
    aligned_image, rotation_angle = correct_orientation(input_image)

    # Save the aligned image to a file
    output_file = "aligned_history_card.jpg"  # Specify the output file name
    cv2.imwrite(output_file, aligned_image)
    
    print(f"Image aligned to {rotation_angle}° and saved as '{output_file}'.")
'''
import cv2
from pytesseract import image_to_osd

def resize_image(image, target_width=800):
    height, width = image.shape[:2]
    aspect_ratio = width / float(height)
    target_height = int(target_width / aspect_ratio)
    resized_image = cv2.resize(image, (target_width, target_height))
    return resized_image

def preprocess_image(image):
    # Convert to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_image

def correct_orientation(image):
    """
    Correct the orientation of a handwritten history card to 0°, 90°, 180°, or 270°.
    Also detects if the image is flipped horizontally or vertically and corrects it.

    Args:
        image (numpy array): Input handwritten history card image.

    Returns:
        aligned_image (numpy array): Image with corrected orientation and flip.
        rotation_angle (int): Angle by which the image was rotated to align (0, 90, 180, 270).
    """
    # Preprocess the image (resize and convert to grayscale)
    image = preprocess_image(image)
    image = resize_image(image)

    # Detect orientation and flip using Tesseract OSD
    osd = image_to_osd(image, output_type="dict")
    rotation_angle = osd.get("rotate", 0)
    is_flipped = osd.get("isFlipped", 0)  # Check if the image is flipped (horizontal or vertical)

    # Rotate the image to the nearest 90-degree orientation
    if rotation_angle == 90:
        aligned_image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
    elif rotation_angle == 180:
        aligned_image = cv2.rotate(image, cv2.ROTATE_180)
    elif rotation_angle == 270:
        aligned_image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    else:
        # No rotation needed
        aligned_image = image

    # Flip the image if needed (check for horizontal/vertical flip)
    if is_flipped:
        aligned_image = cv2.flip(aligned_image, 1)  # Flip horizontally (1 = horizontal, 0 = vertical)

    return aligned_image, rotation_angle


# Example usage
if __name__ == "__main__":
    # Load the handwritten history card image
    input_image = cv2.imread("flip2.PNG")  # Replace with your image file path

    if input_image is None:
        raise FileNotFoundError("The image file was not found. Please check the file path.")

    # Correct orientation and flip
    aligned_image, rotation_angle = correct_orientation(input_image)

    # Save the aligned image to a file
    output_file = "aligned_history_card.jpg"  # Specify the output file name
    cv2.imwrite(output_file, aligned_image)
    
    print(f"Image aligned to {rotation_angle}° and saved as '{output_file}'.")
