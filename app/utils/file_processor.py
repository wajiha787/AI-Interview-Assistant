from fastapi import UploadFile, HTTPException
import PyPDF2
import docx
import io
from typing import str


class FileProcessor:
    """Utility class for processing uploaded files"""
    
    SUPPORTED_TYPES = {
        "application/pdf": "pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
        "text/plain": "txt"
    }
    
    async def process_file(self, file: UploadFile) -> str:
        """
        Process uploaded file and extract text content
        
        Args:
            file: Uploaded file object
            
        Returns:
            str: Extracted text content
            
        Raises:
            HTTPException: If file type is not supported or processing fails
        """
        if file.content_type not in self.SUPPORTED_TYPES:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file.content_type}. Supported types: {list(self.SUPPORTED_TYPES.keys())}"
            )
        
        try:
            # Read file content
            content = await file.read()
            
            # Process based on file type
            file_type = self.SUPPORTED_TYPES[file.content_type]
            
            if file_type == "pdf":
                return self._extract_pdf_text(content)
            elif file_type == "docx":
                return self._extract_docx_text(content)
            elif file_type == "txt":
                return content.decode('utf-8')
            else:
                raise HTTPException(status_code=400, detail="Unsupported file type")
                
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to process file: {str(e)}")
    
    def _extract_pdf_text(self, content: bytes) -> str:
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(content))
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to extract PDF text: {str(e)}")
    
    def _extract_docx_text(self, content: bytes) -> str:
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(io.BytesIO(content))
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to extract DOCX text: {str(e)}")
    
    def validate_file_size(self, file: UploadFile, max_size_mb: int = 10) -> bool:
        """
        Validate file size
        
        Args:
            file: Uploaded file object
            max_size_mb: Maximum file size in MB
            
        Returns:
            bool: True if file size is valid
        """
        # Note: This is a basic check. In production, you might want to check actual file size
        return True  # For now, we'll allow all files

