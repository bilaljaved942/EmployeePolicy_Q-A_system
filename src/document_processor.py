"""Document processing module for PDF extraction and text preprocessing"""
import os
from typing import List, Dict
import re

try:
    import PyPDF2
    PDF_LIB = 'PyPDF2'
except ImportError:
    try:
        import pypdf
        PDF_LIB = 'pypdf'
    except ImportError:
        raise ImportError("Please install PyPDF2 or pypdf: pip install PyPDF2")

from .config import PDF_DIRECTORY, PDF_FILES


class DocumentProcessor:
    """Handles PDF text extraction and preprocessing"""
    
    def __init__(self):
        self.pdf_lib = PDF_LIB
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from a PDF file"""
        try:
            with open(pdf_path, 'rb') as file:
                if self.pdf_lib == 'PyPDF2':
                    reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() + "\n"
                else:
                    reader = pypdf.PdfReader(file)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() + "\n"
                return text
        except Exception as e:
            raise Exception(f"Error reading PDF {pdf_path}: {str(e)}")
    
    def clean_text(self, text: str) -> str:
        """Clean and preprocess extracted text"""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep punctuation
        text = re.sub(r'[^\w\s\.\,\;\:\!\?\-\(\)]', '', text)
        
        # Remove multiple newlines
        text = re.sub(r'\n+', '\n', text)
        
        # Strip leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def process_all_documents(self) -> List[Dict[str, str]]:
        """Process all PDF documents and return structured data"""
        documents = []
        
        for pdf_file in PDF_FILES:
            pdf_path = os.path.join(PDF_DIRECTORY, pdf_file)
            
            if not os.path.exists(pdf_path):
                print(f"Warning: {pdf_path} not found. Skipping...")
                continue
            
            print(f"Processing {pdf_file}...")
            raw_text = self.extract_text_from_pdf(pdf_path)
            cleaned_text = self.clean_text(raw_text)
            
            document = {
                "filename": pdf_file,
                "source": pdf_path,
                "content": cleaned_text,
                "metadata": {
                    "document_type": self._classify_document(pdf_file),
                    "file_size": os.path.getsize(pdf_path)
                }
            }
            
            documents.append(document)
            print(f"  Extracted {len(cleaned_text)} characters from {pdf_file}")
        
        return documents
    
    def _classify_document(self, filename: str) -> str:
        """Classify document type based on filename"""
        filename_lower = filename.lower()
        if "contract" in filename_lower:
            return "employment_contract"
        elif "handbook" in filename_lower or "hr_policy" in filename_lower:
            return "hr_handbook"
        elif "increment" in filename_lower or "probation" in filename_lower:
            return "increment_policy"
        else:
            return "other"
    
    def get_document_statistics(self, documents: List[Dict[str, str]]) -> Dict:
        """Get statistics about processed documents"""
        total_chars = sum(len(doc["content"]) for doc in documents)
        total_words = sum(len(doc["content"].split()) for doc in documents)
        
        return {
            "total_documents": len(documents),
            "total_characters": total_chars,
            "total_words": total_words,
            "average_chars_per_doc": total_chars / len(documents) if documents else 0,
            "average_words_per_doc": total_words / len(documents) if documents else 0
        }


if __name__ == "__main__":
    processor = DocumentProcessor()
    documents = processor.process_all_documents()
    
    print("\n" + "="*60)
    print("Document Processing Summary")
    print("="*60)
    stats = processor.get_document_statistics(documents)
    for key, value in stats.items():
        print(f"{key}: {value}")
    
    print("\nProcessed Documents:")
    for doc in documents:
        print(f"  - {doc['filename']}: {doc['metadata']['document_type']}")
