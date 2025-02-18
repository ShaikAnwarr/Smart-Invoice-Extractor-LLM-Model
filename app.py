import streamlit as st
import os
from PIL import Image
import pytesseract
import json
import re

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Ensure uploads directory exists
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)
HISTORY_FILE = os.path.join(UPLOAD_DIR, "history.json")

# Function to save uploaded file
def save_uploaded_file(uploaded_file):
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

# Function to extract text from image
def extract_text_from_image(image_path, language="eng"):
    image = Image.open(image_path)
    return pytesseract.image_to_string(image, lang=language)

# Load or initialize history
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

# Save extracted text to history
def save_to_history(file_name, extracted_text):
    history = load_history()
    history.append({"file": file_name, "text": extracted_text})
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

# Streamlit UI
st.set_page_config(page_title="Smart Invoice Scanner", layout="wide")
st.title("🧾 Smart Invoice Scanner")

# Sidebar Settings
st.sidebar.header("Settings")
language_map = {"English": "eng", "French": "fra", "German": "deu", "Spanish": "spa", "Chinese": "chi_sim"}
language = st.sidebar.selectbox("Choose OCR Language", list(language_map.keys()), index=0)
selected_lang = language_map[language]

# File Upload Section
st.subheader("📂 Upload an Invoice")
uploaded_file = st.file_uploader("Drag and drop file here or click Browse", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Invoice", use_column_width=True)
    file_path = save_uploaded_file(uploaded_file)

    if st.button("🔍 Extract Text from Invoice"):
        extracted_text = extract_text_from_image(file_path, selected_lang)
        save_to_history(uploaded_file.name, extracted_text)

        st.subheader("Extracted Text:")
        st.text_area("", extracted_text, height=300)

        # Provide Download Option
        st.download_button(
            label="📥 Download Extracted Text",
            data=extracted_text,
            file_name=f"{uploaded_file.name}.txt",
            mime="text/plain"
        )

# Search Extracted Text
st.subheader("🔍 Search in Extracted Invoices")
search_query = st.text_input("Enter text to search:")
if search_query:
    history = load_history()
    results = [entry for entry in history if search_query.lower() in entry["text"].lower()]

    if results:
        st.success(f"Found {len(results)} matching invoices:")
        for result in results:
            highlighted_text = re.sub(f"({search_query})", r"**\1**", result["text"], flags=re.IGNORECASE)
            st.write(f"📄 **File:** {result['file']}")
            st.markdown(highlighted_text)
    else:
        st.warning("No matches found in past invoices.")

# Sidebar - Manage History
st.sidebar.subheader("🗂️ Manage Invoice History")
if st.sidebar.button("📜 View Extracted Invoices"):
    history = load_history()
    if history:
        for entry in history:
            st.sidebar.write(f"📄 {entry['file']}")
    else:
        st.sidebar.warning("No past invoices found.")

if st.sidebar.button("🗑️ Clear History"):
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)
    st.sidebar.success("History Cleared!")
