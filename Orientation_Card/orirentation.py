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
if _name_ == "_main_":
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
