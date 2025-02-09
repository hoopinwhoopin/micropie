from MicroPie import App

import os
from typing import Any

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)  # Ensure upload directory exists

class FileUploadApp(App):

    async def index(self):
        """Serves an HTML form for file uploads."""
        return """<html>
            <head><title>File Upload</title></head>
            <body>
                <h2>Upload a File</h2>
                <form action="/upload" method="post" enctype="multipart/form-data">
                    <input type="file" name="file"><br><br>
                    <input type="submit" value="Upload">
                </form>
            </body>
        </html>"""

    async def upload(self, file):
        # Check for streaming-based attributes:
        if (isinstance(file, dict)
                and "filename" in file
                and "saved_path" in file):
            filename = file["filename"]
            saved_path = file["saved_path"]

            # Optionally, rename the file or do further checks.
            # For instance, you might want to store an original name in your DB or process the file.
            return f"File '{filename}' uploaded successfully, saved to: {saved_path}!"

        # If file data is missing or doesn't match expected structure, return an error.
        return 400, "No file uploaded."

# Run the ASGI app
app = FileUploadApp()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

