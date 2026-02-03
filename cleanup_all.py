"""
Complete cleanup script - deletes all vector DB data
"""
import shutil
import os

# Delete entire vector_db directory
if os.path.exists("./vector_db"):
    shutil.rmtree("./vector_db")
    print("✓ Deleted ./vector_db directory")

# Recreate empty vector_db directory
os.makedirs("./vector_db", exist_ok=True)
print("✓ Recreated ./vector_db directory (empty)")

# Delete all user uploads
uploads_path = "./uploads"
if os.path.exists(uploads_path):
    for user_folder in os.listdir(uploads_path):
        user_path = os.path.join(uploads_path, user_folder)
        if os.path.isdir(user_path):
            shutil.rmtree(user_path)
            print(f"✓ Deleted {user_path}")

print("\n✓ Complete cleanup done! All documents removed.")
