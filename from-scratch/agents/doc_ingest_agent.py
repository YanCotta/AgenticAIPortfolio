import os
import docx
import PyPDF2
from .base_agent import BaseAgent

class DocumentIngestionAgent(BaseAgent):
    def __init__(self):
        super().__init__("DocumentIngestionAgent")

    def _extract_text_from_txt(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()

    def _extract_text_from_pdf(self, file_path):
        with open(file_path, "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            return " ".join([page.extract_text() for page in reader.pages if page.extract_text()])

    def _extract_text_from_docx(self, file_path):
        doc = docx.Document(file_path)
        return " ".join([para.text for para in doc.paragraphs])

    def process(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} not found.")

        file_ext = file_path.split(".")[-1].lower()
        extractors = {"txt": self._extract_text_from_txt, "pdf": self._extract_text_from_pdf, "docx": self._extract_text_from_docx}

        if file_ext not in extractors:
            raise ValueError(f"Unsupported file type: {file_ext}")

        text = extractors[file_ext](file_path)
        return {"text": text.strip(), "metadata": {"file_name": os.path.basename(file_path), "file_type": file_ext}}
