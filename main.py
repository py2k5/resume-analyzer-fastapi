from fastapi import FastAPI, UploadFile, File
import fitz


app = FastAPI()

@app.get("/")
def home():
    return {"message": "Resume Analyzer API is running"}

@app.post("/analyze")
async def analyze_resume(file: UploadFile = File(...)):
    text: str = ""

    if file.filename.endswith(".pdf"):
        doc = fitz.open(stream=await file.read(), filetype="pdf")
        for page in doc:
            text += page.get_text()

        # Add your analyzer logic here
    return { "file_name": file.filename, "content_length": len(text) }



