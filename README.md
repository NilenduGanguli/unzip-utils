# Document Store API

This is a simple FastAPI application that acts as a document store.

## Docker Setup (Recommended)

To run the application in a Docker container within its own network:

1. Build and run with Docker Compose:
   ```bash
   docker-compose up --build
   ```

The application will be available at `http://localhost:8000`.

## Local Installation (Alternative)

1. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

Run the application using uvicorn:

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

## API Usage

Since JSON does not support raw binary data, the documents must be **Base64 encoded** strings.

### 1. Upload a Document

**Endpoint:** `POST /upload`

**Request Body:**
```json
{
  "content": "<base64_encoded_string>"
}
```

**Response:**
```json
{
  "document_link_id": "unique-uuid-string"
}
```

### 2. Fetch a Document

**Endpoint:** `POST /fetch`

**Request Body:**
```json
{
  "document_link_id": "unique-uuid-string"
}
```

**Response:**
```json
{
  "content": "<base64_encoded_string>"
}
```

## Example with Python

```python
import requests
import base64

# 1. Upload
text_content = "Hello World".encode('utf-8')
b64_content = base64.b64encode(text_content).decode('utf-8')

response = requests.post("http://127.0.0.1:8000/upload", json={"content": b64_content})
print("Upload Response:", response.json())

doc_id = response.json().get("document_link_id")

# 2. Fetch
response = requests.post("http://127.0.0.1:8000/fetch", json={"document_link_id": doc_id})
data = response.json()
print("Fetch Response:", data)

# Decode back
fetched_content = base64.b64decode(data["content"])
print("Decoded Content:", fetched_content.decode('utf-8'))
```
