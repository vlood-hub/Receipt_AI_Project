from google import genai
from openai import OpenAI

AI_INSTRUCTIONS = """
- If the languange is not english, traslate it to english
- Always check the grammar
- Check the item name to see whether it matches the name of the same item on the internet. If it doesn't, replace it
- Output should be in json-format
"""

PROMPT = """
    Extract the following information:
    - customer id
    - receipt number
    - order date
    - total sum
    - item (name, number, amount, price, currency)
    """


def gemini_response(base64_obj, file_mime_type):
    client = genai.Client(api_key="AIzaSyBqvKj0CZI3TMkrInL5g57JN4AilBShoUU")
    generation_config = {"system_instruction": AI_INSTRUCTIONS}

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        config=generation_config,
        contents=[
            # 1. Text Prompt
            {
                # For clarity in multimodal requests, content is often wrapped in 'parts'
                "parts": [
                    {"text": PROMPT}
                ]
            },
            # 2. File Input (Dynamically one of PNG, JPEG, or PDF)
            {
                # The keys used here ('inline_data', 'mime_type') align with the structure
                # often seen in the Google Generative AI SDK for binary data.
                "inline_data": {
                    # This MUST be correctly set by your calling logic based on the file type:
                    # 'image/png', 'image/jpeg', or 'application/pdf'
                    "mime_type": file_mime_type,

                    # This holds the Base64 data of the single file being sent
                    "data": base64_obj
                }
            }
        ]
    )

    result = response.text

    return result


def chatgpt_response(base64_obj, file_mime_type):

    client = OpenAI(
        api_key="sk-proj-kMSAyPBsgR8W8g_LODV3vBDGsyfMVuS-"
                "VUagT1Tcea4rpCtUOH9yENfuF81LHklkv26RQBAYmQT3BlbkFJVm2vnF1bOji8hrcl0O02-"
                "qvwJkyrFPsEtmMO5lWiB8LBD63qPakCPU2vX26l4VLXznAz7SYA8A"
    )

    response = client.responses.create(
        model="gpt-5-nano",
        instructions=AI_INSTRUCTIONS,
        input=[
            # 1. Text
            {
                "type": "text",
                "text": PROMPT
            },
            # 2. PNG Image
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/png",
                    "data": base64_obj
                }
            },
            # 3. JPEG Image
            {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": base64_obj
                }
            },
            # 4. PDF Document
            {
                "type": "file", # or 'document' depending on the API
                "source": {
                    "type": "base64",
                    "media_type": "application/pdf",
                    "data": base64_obj
                }
            }
        ]
    )

    result = response.text

    return result