import re


def chunk_pages(pages, max_chars=3800, overlap=450):
    out = []

    for page in pages:
        text = page["text"]
        document_name = page.get("document_name", "")
        page_number = page["page_number"]

        paras = [
            p.strip()
            for p in re.split(r"\n\s*\n", text)
            if p.strip()
        ]

        buf = ""

        for para in paras:
            if len(para) > max_chars:
                if buf:
                    out.append((buf, page_number, document_name))
                    buf = ""

                start = 0
                while start < len(para):
                    chunk = para[start:start + max_chars]
                    out.append((chunk, page_number, document_name))
                    start = max(start + max_chars - overlap, start + 1)

                continue

            if buf and len(buf) + len(para) + 2 > max_chars:
                out.append((buf, page_number, document_name))
                buf = buf[-overlap:] + "\n\n" + para if overlap else para
            else:
                buf = (buf + "\n\n" + para).strip()

        if buf:
            out.append((buf, page_number, document_name))

    return [
        {
            "id": f"chunk-{i + 1:05d}",
            "document_name": document_name,
            "page_start": page_number,
            "page_end": page_number,
            "text": text
        }
        for i, (text, page_number, document_name) in enumerate(out)
    ]
