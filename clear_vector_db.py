import chromadb
import shutil
import os

# Delete vector_db directory completely
db_path = './vector_db'
if os.path.exists(db_path):
    shutil.rmtree(db_path)
    print(f"Deleted {db_path} directory")

# Recreate the directory
os.makedirs(db_path, exist_ok=True)
print(f"Recreated {db_path} directory")

# Verify it's empty
client = chromadb.PersistentClient(path=db_path)
collections = client.list_collections()
print(f"\nCollections in vector_db: {len(collections)}")
if len(collections) > 0:
    print("Collections found:")
    for col in collections:
        print(f"  - {col.name}")
else:
    print("Vector database is clean - no collections")
