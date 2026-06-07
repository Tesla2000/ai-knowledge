from __future__ import annotations

from pathlib import Path

import PyPDF2


def remove_blank_page(pdf_path: Path):
    with pdf_path.open("rb") as file:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter()

        num_pages = len(reader.pages)

        for page_num in range(num_pages == 4, num_pages):
            page = reader.pages[page_num]
            writer.add_page(page)

    with pdf_path.open("wb") as output_file:
        writer.write(output_file)
