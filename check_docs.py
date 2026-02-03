from src.models import get_db, Document

db = next(get_db())
docs = db.query(Document).filter(Document.user_id == 1).all()
print(f"User 1 has {len(docs)} documents:")
for doc in docs:
    print(f"  - {doc.original_filename} (ID: {doc.id})")
