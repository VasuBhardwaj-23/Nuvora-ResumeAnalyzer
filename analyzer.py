import os
import logging
import fitz  # PyMuPDF
import json
import gc
from pathlib import Path
from PIL import Image
import google.generativeai as genai

# -----------------------------
# Gemini API Setup (Directly in Code)
# -----------------------------
api_key = "AIzaSyAuVXebsNDvV8LN2XIZm0EoS1vPI1mjlF8"  # 🔑 apni key yahan daal
genai.configure(api_key=api_key)

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logging.info("🚀 Starting the script...")
logging.info("✅ GenAI API configured successfully (Colab Optimized).")

# -----------------------------
# PDF → Image Conversion
# -----------------------------
def pdf_to_jpg(pdf_path, output_folder="pdf_images", dpi=200):
    """Converts each page of a PDF into a JPG image and saves it."""
    logging.info(f"📄 Converting PDF '{pdf_path}' to images...")
    file_paths = []
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)

    try:
        pdf_document = fitz.open(pdf_path)
        total_pages = len(pdf_document)
        logging.info(f"📘 Opened PDF with {total_pages} pages.")

        for page_number in range(total_pages):
            page = pdf_document[page_number]
            pix = page.get_pixmap(dpi=dpi)
            output_file = output_folder / f"page_{page_number + 1}.jpg"
            pix.save(output_file)
            del pix
            file_paths.append(str(output_file))
            logging.info(f"✅ Saved image: {output_file}")

        pdf_document.close()
    except Exception as e:
        logging.error(f"⚠️ Error converting PDF to images: {str(e)}")

    return file_paths

# -----------------------------
# Process Image / Text with Gemini
# -----------------------------
def process_image(file_path="", prompt="Extract text and structure from this image.", type=None):
    """Uses Gemini model to process images or text and return structured JSON."""
    logging.info(f"🚀 Processing file: {file_path} | Type: {type}")

    try:
        # ✅ Use the latest working model
        model = genai.GenerativeModel("models/gemini-2.5-flash")

        # Handle both image and text
        if type == "image":
            img = Image.open(file_path)
            response = model.generate_content([prompt, img])
        elif type == "text":
            response = model.generate_content(prompt)
        else:
            return {"error": "Invalid type."}

        # Handle response
        if not response:
            return {"error": "Empty response."}

        # Extract text safely
        text_output = getattr(response, "text", "").strip()

        if not text_output:
            return {"error": "No text extracted from response."}

        clean_text = text_output.replace("```json", "").replace("```", "").strip()

        try:
            parsed_data = json.loads(clean_text)
            with open("result.json", "w", encoding="utf-8") as f:
                json.dump(parsed_data, f, indent=4, ensure_ascii=False)
            logging.info("✅ Parsed JSON successfully and saved to result.json.")
            return parsed_data
        except json.JSONDecodeError:
            logging.warning("⚠️ Could not parse JSON. Returning raw text instead.")
            return {"raw_text": clean_text}

    except Exception as e:
        logging.error(f"❌ Error processing image/text: {str(e)}")
        return {"error": str(e)}

    finally:
        gc.collect()

# -----------------------------
# Test Execution in Colab
# -----------------------------
if __name__ == "__main__":
    test_pdf = "resume.pdf"  # 🔹 apna uploaded resume yahan likh
    logging.info(f"🔍 Testing PDF conversion for: {test_pdf}")
    images = pdf_to_jpg(test_pdf)
    if images:
        logging.info(f"Extracted {len(images)} images successfully.")
        print(f"✅ Extracted {len(images)} images: {images}")
        for img in images:
            print(f"🖼 Processing {img} ...")
            result = process_image(img, type="image")
            print(result)
    else:
        logging.error("❌ No images extracted during test.")
        print("❌ No images extracted.")
