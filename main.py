from fastapi import FastAPI, UploadFile, File
import fitz

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Resume Analyzer API is running"}

@app.post("/analyze")
async def analyze_resume(file: UploadFile = File(...)):
    text = ""

    if file.filename.endswith(".pdf"):
        file_content = await file.read()
        doc = fitz.open(stream=file_content, filetype="pdf")
        for page in doc:
            text += page.get_text()
        doc.close()

        # Add your analyzer logic here
    return { "file_name": file.filename, "content_length": len(text) }



