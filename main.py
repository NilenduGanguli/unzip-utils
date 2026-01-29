import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uuid
import base64
import random
import string
import json
import os
import aiofiles
from typing import Dict

app = FastAPI()

# Configuration
STORAGE_PATH = "/data/documents"
os.makedirs(STORAGE_PATH, exist_ok=True)

class DocumentUploadRequest(BaseModel):
    # Base64 encoded byte array
    content: str
    filename: str | None = None

class DocumentUploadResponse(BaseModel):
    document_link_id: str

class DocumentFetchRequest(BaseModel):
    document_link_id: str

class DocumentFetchResponse(BaseModel):
    # Base64 encoded byte array
    content: str
    filename: str | None = None

def generate_document_id(length=10):
    """Generate a random alphanumeric ID of specified length."""
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def get_file_path(document_id: str):
    return os.path.join(STORAGE_PATH, document_id)

@app.post("/upload", response_model=DocumentUploadResponse)
async def upload_document(request: DocumentUploadRequest):
    try:
        # Decode base64 to bytes
        file_bytes = base64.b64decode(request.content)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid base64 content")
    
    # Generate a unique 10-char alphanumeric ID
    # ensuring no collision (though simple random is usually enough for 10 chars)
    while True:
        document_link_id = generate_document_id()
        file_path = get_file_path(document_link_id)
        if not os.path.exists(file_path):
            break
    
    # Store the document to disk
    async with aiofiles.open(file_path, 'wb') as f:
        await f.write(file_bytes)
    
    # Store metadata
    meta_path = file_path + ".meta"
    metadata = {"filename": request.filename}
    try:
        async with aiofiles.open(meta_path, 'w') as f:
            await f.write(json.dumps(metadata))
    except Exception:
        # If metadata write fails, we proceed (or we could log it)
        pass
    
    #artificial delay to simulate processing time
    await asyncio.sleep(1)
    
    return DocumentUploadResponse(document_link_id=document_link_id)

@app.post("/fetch", response_model=DocumentFetchResponse)
async def fetch_document(request: DocumentFetchRequest):
    document_link_id = request.document_link_id
    file_path = get_file_path(document_link_id)
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Document not found")
    
    try:
        async with aiofiles.open(file_path, 'rb') as f:
            file_bytes = await f.read()
        
        # Try to read metadata
        filename = None
        meta_path = file_path + ".meta"
        if os.path.exists(meta_path):
            try:
                async with aiofiles.open(meta_path, 'r') as f:
                    content = await f.read()
                    metadata = json.loads(content)
                    filename = metadata.get("filename")
            except Exception:
                pass
        
        #artificial delay to simulate processing time
        await asyncio.sleep(1)
        
        # Encode back to base64 for the response
        content_b64 = base64.b64encode(file_bytes).decode('utf-8')
        return DocumentFetchResponse(content=content_b64, filename=filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading document: {str(e)}")

# Health check
@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
