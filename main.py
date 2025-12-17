import os
import base64
import json
import ai_response

BASE_DIR = "data"
SUB_DIR = "receipts"
LOAD_PATH = os.path.join(BASE_DIR, SUB_DIR)
SAVE_PATH = os.path.join(BASE_DIR, 'receipts.json')

# def load_receips():
#     """Loads the local registry of trained model IDs."""
#     if not os.path.exists(LOAD_PATH):
#         return {}
#     try:
#         with open(LOAD_PATH, 'r', encoding='utf-8') as f:
#             return json.load(f)
#     except (json.JSONDecodeError, IOError):
#         print("Warning: Could not read or decode model registry. Starting fresh.")
#         return {}


def save_receipts_to_json(receipts):
    """Saves the receips to json."""
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    with open(SAVE_PATH, 'w', encoding='utf-8') as f:
        json.dump(receipts, f, indent=4)
    print(f"Receipts saved in: {SAVE_PATH}")


def encode_local_file_to_base64_and_get_mime(full_file_path):
    """Loads the file, encodes it, and determines the MIME type."""
    if not os.path.exists(full_file_path):
        return None, None

    # 1. Determine the MIME Type based on the extension
    ext = os.path.splitext(full_file_path)[1].lower() # Gets the extension (e.g., '.png')

    # Simple mapping for common types
    mime_type_map = {
        '.png': 'image/png',
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.pdf': 'application/pdf',
        # Add other types as needed
    }

    mime_type = mime_type_map.get(ext)

    if not mime_type:
        print(f"Warning: Unknown file type for extension {ext}")
        return None, None

    # 2. Encode the file content
    with open(full_file_path, "rb") as f:
        base64_data = base64.b64encode(f.read()).decode("utf-8")

    # Return both the data and the MIME type required by the API
    return base64_data, mime_type


def main():

    for filename in os.listdir(LOAD_PATH):
        # Construct the full absolute path to the file
        full_file_path = os.path.join(LOAD_PATH, filename)
        base64_obj, mime_type = encode_local_file_to_base64_and_get_mime(full_file_path)
        text = ai_response.gemini_response(base64_obj, mime_type)
    save_receipts_to_json(text)

    print(text)


if __name__ == "__main__":
    main()