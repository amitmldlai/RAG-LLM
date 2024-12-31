import fitz  # PyMuPDF
import base64
from io import BytesIO
from PIL import Image
import requests
from typing import List
import os


API_URL = "https://api.openai.com/v1/chat/completions"


def pdf_to_base64_images(pdf_path: str) -> List[str]:
    """Converts each page of the PDF to a Base64-encoded PNG image."""
    base64_images = []
    try:
        pdf_document = fitz.open(pdf_path)

        for page_number in range(len(pdf_document)):
            page = pdf_document[page_number]
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

            buffered = BytesIO()
            img.save(buffered, format="PNG")  # Save as PNG
            img_data = buffered.getvalue()  # Get the byte data
            base64_image = base64.b64encode(img_data).decode('utf-8')
            base64_images.append(base64_image)

    except Exception as e:
        print(f"Error converting PDF to Base64 images: {e}")

    return base64_images


def image_to_text(base64_image: str) -> str:
    """Extracts text and URLs from the Base64 image using OpenAI's API."""
    payload = {
        "model": "gpt-4o",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": """
"Extract the text and structure from the image in the format shown below. 
Pay special attention to maintaining the layout, section titles, bullet points, 
numbering, and any handwritten content. Reproduce stars and rating scales accurately, 
and format responses to questions clearly as shown in the image.

Notes:
   1. Ensure that handwritten content is captured where indicated, and maintain any stylized formatting (like stars for pain ratings).
   2. Keep all section titles and their subheadings.
   3. Maintain the spacing and indentation where appropriate.
   4. Reproduce the handwritten content as accurately as possible based on OCR or estimation."
   5. Do not include anything from your end, only provide the extracted text
                                 """
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 1000
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('GRAPHRAG_API_KEY')}"
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()['choices'][0]['message']['content']

    except requests.exceptions.RequestException as e:
        print(f"API request error: {e}")
        return ""  # Return an empty string on error


def make_text_file(input_path, pdf_filename: str):
    text = ""
    """Main function to process the PDF and extract text from each page."""
    pdf_path = os.path.join('uploads', pdf_filename)
    base64_images = pdf_to_base64_images(pdf_path)
    filename = pdf_filename.split('.')[0]
    for idx, base64_img in enumerate(base64_images):
        text = text + image_to_text(base64_img) + '\n'
    with open(f'{input_path}/{filename}.txt', 'w', encoding='utf-8') as file:
        file.write(text)




