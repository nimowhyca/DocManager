# upload document
# --> uploaded_file, tags, document, date
# --> uploaded_file --> test.pdf
# --> uploaded_file --> test.pdf --> thumbnail
# --> uploaded_file --> folder with the same name as pdf file --> test --> extract all images -> 0.jpg, 1.jpg
# --> uploaded_file -> total pages
# upload_date -> time, datetime

from db.repository import DocumentRepository
from core.file_manager import FileManager
from core.thumbnail import ThumbnailGenerator

class DocumentService:
    def __init__(self):
        self.repo =DocumentRepository()
        self.file_manager = FileManager()
        self.thumbnail_generator = ThumbnailGenerator()

    def upload_document(self, uploaded_file, tags, description, lecture_date=None):
        
        doc = []

        # 1. Save file
        file_path = self.file_manager.save_file(uploaded_file)
        
        # 2. Generate thumbnail
        thumbnail_path = self.thumbnail_generator.generate_thumbnail(file_path)
        
        # 3. Get total pages
        total_pages = self.thumbnail_generator.get_total_pages(file_path)
        
        # 4. Convert to images
        # 5. create required variables : upload date

        # 6. Save to db
        # self.repo.add_document(doc)
