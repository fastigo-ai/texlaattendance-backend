# import uuid
# from pathlib import Path

# UPLOAD_DIR = Path("uploads")
# UPLOAD_DIR.mkdir(exist_ok=True)

# def save_file(file_content: bytes, filename: str) -> str:

#     file_id = str(uuid.uuid4())
#     extension = filename.split('.')[-1]

#     new_filename = f"{file_id}.{extension}"

#     file_path = UPLOAD_DIR / new_filename

#     with open(file_path, "wb") as f:
#         f.write(file_content)

#     return str(file_path)
import cloudinary.uploader

async def upload_to_cloudinary(file, employee_id: str, category: str):
    folder_path = f"texla/employees/{employee_id}/{category}"
    result = cloudinary.uploader.upload(
        file.file,
        folder=folder_path
    )

    return result["secure_url"]