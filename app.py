import os
import logging
import base64
import io
from flask import Flask, render_template, request, jsonify, url_for
from utils.image_processor import remove_background

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")


# @app.route('/docs')
# def docs():
#     """Render the API documentation page."""
#     return render_template('docs.html')


@app.route('/api/remove-background', methods=['POST'])
def process_image():
    """API endpoint to remove the background from an image.

    Expects:
        - A JSON payload with a base64 encoded image in the 'image' field

    Returns:
        - A JSON response with the processed base64 image or an error message
    """
    try:
        data = request.get_json()

        if not data or 'image' not in data:
            return jsonify({'error': 'No image provided'}), 400

        # Get the base64 image from the request
        base64_image = data['image']

        # Check if the base64 string starts with a data URL prefix and remove it if it does
        if ',' in base64_image:
            base64_image = base64_image.split(',', 1)[1]

        try:
            # Process the image
            processed_image = remove_background(base64_image)
            return jsonify({'image': processed_image})
        except Exception as e:
            logger.error(f"Error processing image: {e}")
            return jsonify({'error': f'Error processing image: {str(e)}'}), 500

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500


# Error handlers
@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({'error': 'Server error'}), 500


if __name__ == '__main__':
    app.run()
