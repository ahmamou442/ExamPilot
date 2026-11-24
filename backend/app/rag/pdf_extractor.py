import fitz
def extract_pdf(data:bytes, filename:str):
    doc=fitz.open(stream=data, filetype="pdf")
    pages=[]
    for i,p in enumerate(doc, start=1):
        text=p.get_text("text") or ""
        if text.strip(): pages.append({"document_name":filename,"page_number":i,"text":text})
    if not pages: raise ValueError("No extractable text found. Scanned PDFs/OCR are not supported yet.")
    return pages
