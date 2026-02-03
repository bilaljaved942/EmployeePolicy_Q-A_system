import chromadb

client = chromadb.PersistentClient(path='./vector_db')

# Delete both collections
for col_name in ['user_1_documents', 'user_2_documents']:
    try:
        client.delete_collection(name=col_name)
        print(f'Deleted collection: {col_name}')
    except Exception as e:
        print(f'Error deleting {col_name}: {e}')

print('\nRemaining collections:')
collections = client.list_collections()
for col in collections:
    print(f'  - {col.name}')
