from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
import shutil
import os

from redactor import redact_docx

app = FastAPI(
    title="PII Redaction Platform",
    version="1.0"
)

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.get("/")
def home():
    return {"message": "PII Redaction API Running"}

@app.post("/redact")
async def redact(file: UploadFile = File(...)):

    input_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    output_path, entity_counts = redact_docx(input_path)

    print("\nDetected Entities:")
    print(entity_counts)
    return FileResponse(
    output_path,
    filename=os.path.basename(output_path)
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)