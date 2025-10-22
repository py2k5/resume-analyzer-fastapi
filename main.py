from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import fitz  # PyMuPDF

app = FastAPI()

# Serve static files (CSS)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Templates folder for HTML
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/analyze")
async def analyze_resume(file: UploadFile = File(...)):
    try:
        text = ""
        if file.filename.endswith(".pdf"):
            doc = fitz.open(stream=await file.read(), filetype="pdf")
            for page in doc:
                text += page.get_text()

        # Simple keyword detection demo
        keywords = ["Python", "AWS", "FastAPI", "SQL", "Machine Learning"]
        found = [k for k in keywords if k.lower() in text.lower()]

        return JSONResponse({
            "filename": file.filename,
            "content_length": len(text),
            "found_skills": found
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
