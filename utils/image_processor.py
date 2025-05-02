import base64
import io
from PIL import Image
from rembg import remove
import logging

logger = logging.getLogger(__name__)

def remove_background(base64_image):
    """Removes the background from an image using rembg.

    Args:
        base64_image (str): Base64 encoded image string

    Returns:
        str: Base64 encoded image with background removed

    Raises:
        ValueError: If the input is not a valid base64 encoded image
    """
    try:
        # Decode the base64 image
        image_data = base64.b64decode(base64_image)

        # Open the image using PIL
        input_image = Image.open(io.BytesIO(image_data))

        # Process the image with rembg
        logger.debug(f"Processing image of format: {input_image.format}")
        logger.debug(f"Image size: {input_image.size}")

        # Convert to RGB mode if the image is not in RGB or RGBA mode
        if input_image.mode not in ["RGB", "RGBA"]:
            input_image = input_image.convert("RGB")

        # Remove the background
        output_image = remove(input_image)

        # Save the processed image to a bytes buffer
        output_buffer = io.BytesIO()

        # Preserve the original format if possible
        image_format = input_image.format if input_image.format else "PNG"

        # If the result is RGBA, we need to save as PNG to preserve transparency
        if output_image.mode == "RGBA":
            image_format = "PNG"

        output_image.save(output_buffer, format=image_format)
        output_buffer.seek(0)

        # Encode the processed image to base64
        processed_base64 = base64.b64encode(output_buffer.getvalue()).decode('utf-8')

        # Add the appropriate data URL prefix
        mime_type = f"image/{image_format.lower()}"
        data_url = f"data:{mime_type};base64,{processed_base64}"

        return data_url

    except base64.binascii.Error:
        logger.error("Invalid base64 encoding")
        raise ValueError("Invalid base64 encoding")

    except Image.UnidentifiedImageError:
        logger.error("Could not identify image format")
        raise ValueError("Could not identify image format")

    except Exception as e:
        logger.error(f"Error processing image: {e}")
        raise ValueError(f"Error processing image: {str(e)}")
