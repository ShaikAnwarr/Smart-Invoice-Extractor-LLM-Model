import google.generativeai as genai
import os
from PIL import Image
from tkinter import Tk, filedialog
from dotenv import load_dotenv

# Load API Key from environment file
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Configure Gemini API
genai.configure(api_key=GOOGLE_API_KEY)


# Function to select file using File Dialog
def select_file():
    root = Tk()
    root.withdraw()  # Hide the root Tkinter window
    file_path = filedialog.askopenfilename(
        title="Select Invoice Image",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
    )
    return file_path


# Function to extract invoice data using Gemini Vision
def extract_invoice_data(image_path):
    if not image_path:
        print("No file selected!")
        return None

    try:
        img = Image.open(image_path)

        # Call Gemini Pro Vision API
        model = genai.GenerativeModel("gemini-pro-vision")
        response = model.generate_content([img])
        extracted_text = response.text

        return extracted_text
    except Exception as e:
        print(f"Error extracting data: {e}")
        return None


if __name__ == "__main__":
    invoice_image = select_file()

    if invoice_image:
        extracted_text = extract_invoice_data(invoice_image)
        if extracted_text:
            print("Extracted Invoice Data:\n", extracted_text)
        else:
            print("Failed to extract data.")
    else:
        print("No image selected. Exiting program.")
