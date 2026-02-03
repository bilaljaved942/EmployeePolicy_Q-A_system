import chromadb

client = chromadb.PersistentClient(path='./vector_db')

for col_name in ['user_1_documents', 'user_2_documents']:
    print(f'\n{col_name}:')
    col = client.get_collection(name=col_name)
    results = col.get(limit=100)
    
    # Get unique sources
    sources = set()
    user_ids = set()
    for metadata in results['metadatas']:
        source = metadata.get('source', 'Unknown')
        user_id = metadata.get('user_id', 'None')
        sources.add(source)
        user_ids.add(str(user_id))
    
    print(f'  Total chunks: {col.count()}')
    print(f'  Sources: {sources}')
    print(f'  User IDs in metadata: {user_ids}')
    
    # Check first few metadata
    if results['metadatas']:
        print(f'  First metadata: {results["metadatas"][0]}')
