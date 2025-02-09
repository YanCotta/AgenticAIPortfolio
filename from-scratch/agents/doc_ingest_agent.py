import os
import mimetypes
import docx
import PyPDF2
from bs4 import BeautifulSoup  # for HTML parsing
from ebooklib import epub    # for EPUB parsing
from .base_agent import BaseAgent

class DocumentIngestionAgent(BaseAgent):
    CHUNK_SIZE = 1024 * 1024  # 1 MB chunks

    def __init__(self):
        super().__init__("DocumentIngestionAgent")

    def _detect_mime_type(self, file_path):
        mime, _ = mimetypes.guess_type(file_path)
        return mime

    def _validate_file(self, file_path):
        if os.path.getsize(file_path) == 0:
            raise ValueError(f"File {file_path} is empty or corrupted.")
        return True

    def _extract_text_from_txt(self, file_path):
        text = ""
        file_size = os.path.getsize(file_path)
        processed = 0
        with open(file_path, 'r', encoding='utf-8') as file:
            while True:
                chunk = file.read(self.CHUNK_SIZE)
                if not chunk:
                    break
                text += chunk
                processed += len(chunk)
                self.logger.info(f"Processed {processed/file_size*100:.2f}% of txt file")
        return text

    def _extract_text_from_pdf(self, file_path):
        text = ""
        with open(file_path, "rb") as pdf_file:
            reader = PyPDF2.PdfReader(pdf_file)
            for i, page in enumerate(reader.pages):
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
                self.logger.info(f"Processed page {i+1}/{len(reader.pages)}")
        return text

    def _extract_text_from_docx(self, file_path):
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])
        self.logger.info("Extracted text from docx")
        return text

    def _extract_text_from_html(self, file_path):
        text = ""
        file_size = os.path.getsize(file_path)
        processed = 0
        with open(file_path, 'r', encoding='utf-8') as file:
            for chunk in iter(lambda: file.read(self.CHUNK_SIZE), ""):
                soup = BeautifulSoup(chunk, 'html.parser')
                text += soup.get_text(separator="\n")
                processed += len(chunk)
                self.logger.info(f"Processed {processed/file_size*100:.2f}% of html file")
        return text

    def _extract_text_from_epub(self, file_path):
        text = ""
        book = epub.read_epub(file_path)
        for item in book.get_items():
            if item.get_type() == epub.EpubHtml:
                soup = BeautifulSoup(item.get_content(), 'html.parser')
                text += soup.get_text(separator="\n")
        self.logger.info("Extracted text from epub")
        return text

    def _extract_metadata(self, file_path):
        stats = os.stat(file_path)
        return {"file_name": os.path.basename(file_path), "size": stats.st_size, "modified": stats.st_mtime}

    def process(self, file_path):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File {file_path} not found.")

        self._validate_file(file_path)
        mime = self._detect_mime_type(file_path)
        self.logger.info(f"Detected MIME type: {mime}")

        if mime:
            if mime.startswith("text/plain"):
                extractor = self._extract_text_from_txt
            elif mime == "application/pdf":
                extractor = self._extract_text_from_pdf
            elif mime == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
                extractor = self._extract_text_from_docx
            elif mime == "text/html":
                extractor = self._extract_text_from_html
            elif mime == "application/epub+zip":
                extractor = self._extract_text_from_epub
            else:
                raise ValueError(f"Unsupported MIME type: {mime}")
        else:
            ext = file_path.split(".")[-1].lower()
            mapping = {
                "txt": self._extract_text_from_txt,
                "pdf": self._extract_text_from_pdf,
                "docx": self._extract_text_from_docx,
                "html": self._extract_text_from_html,
                "epub": self._extract_text_from_epub
            }
            if ext not in mapping:
                raise ValueError(f"Unsupported file extension: {ext}")
            extractor = mapping[ext]

        text = extractor(file_path)
        if not text.strip():
            raise ValueError("Extracted text is empty, possible corruption.")
        metadata = self._extract_metadata(file_path)
        return {"text": text.strip(), "metadata": metadata}
