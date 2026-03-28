from db.database import get_connection
from core.models import Document

class DocumentRepository:
    
    def add_document(self, doc: Document):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO documents (
            name, path, thumbnail_path, tags, description,
            upload_date, lecture_date, total_pages
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            doc.name,
            doc.path,
            doc.thumbnail_path,
            doc.tags,
            doc.description,
            doc.upload_date,
            doc.lecture_date,
            doc.total_pages
        ))

        conn.commit()
        conn.close()

    def search_documents(self, tag=None, date=None):
        conn = get_connection()
        cursor = conn.cursor()

        query = "SELECT * FROM documents"
        conditions = []
        params = []

        # WHERE , OR

        if tag:
            conditions.append("tags LIKE ?")
            params.append(f"%{tag}%")

        if date:
            conditions.append("lecture_date = ?")
            params.append(date)
        
        if conditions:
            # last_part_query = " OR ".join(conditions)
            # query += " WHERE " 
            # query+=last_part_query

            query += " WHERE " + " OR ".join(conditions)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        conn.close()

        # list of document objects
        return [Document(*row) for row in rows]
    

        




