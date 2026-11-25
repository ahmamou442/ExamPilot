import fitz


def extract_pdf(data: bytes, filename: str, *, ocr: bool = True, min_text_chars: int = 25) -> list[dict[str, object]]:
    """Extract native PDF text and optionally OCR sparse/scanned pages.

    OCR is optional at runtime: text-based PDFs work without Tesseract installed.
    Scanned pages produce an actionable error if the optional OCR dependency is absent.
    """
    pages: list[dict[str, object]] = []
    try:
        document = fitz.open(stream=data, filetype="pdf")
    except (fitz.FileDataError, RuntimeError) as exc:
        raise ValueError(f"{filename} is not a valid or readable PDF.") from exc
    try:
        for number, page in enumerate(document, start=1):
            text = (page.get_text("text") or "").strip()
            if len(text) < min_text_chars and ocr:
                try:
                    import pytesseract
                    from PIL import Image
                    from io import BytesIO
                    pixmap = page.get_pixmap(matrix=fitz.Matrix(2, 2), alpha=False)
                    image = Image.open(BytesIO(pixmap.tobytes("png")))
                    recognized = pytesseract.image_to_string(image).strip()
                    if len(recognized) > len(text):
                        text = recognized
                except ImportError as exc:
                    if not text:
                        raise ValueError("This PDF appears to be scanned. Install Tesseract OCR and the optional pytesseract/Pillow packages, or upload a text-based PDF.") from exc
                except Exception as exc:
                    if not text:
                        raise ValueError(f"OCR could not read page {number} of {filename}. Check the Tesseract installation and try again.") from exc
            if text:
                pages.append({"document_name": filename, "page_number": number, "text": text})
    finally:
        document.close()
    if not pages:
        raise ValueError("No readable text found in this PDF. For scanned PDFs, install Tesseract OCR and the optional OCR dependencies.")
    return pages
