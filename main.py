from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from utils.textract_service import get_textract_service
from utils.skill_extractor import SkillExtractor
from utils.certification_extractor import CertificationExtractor
import logging

app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize extractors
skill_extractor = SkillExtractor()
certification_extractor = CertificationExtractor()

# Initialize Textract service
try:
    textract_service = get_textract_service()
    logger.info("AWS Textract service initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Textract service: {e}")
    textract_service = None

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
        # Check if Textract service is available
        if textract_service is None:
            return JSONResponse({
                "error": "AWS Textract service is not available. Please check your AWS configuration."
            }, status_code=503)
        
        # Validate file type
        if not file.filename.lower().endswith(('.pdf', '.png', '.jpg', '.jpeg', '.tiff')):
            return JSONResponse({
                "error": "Unsupported file format. Please upload PDF, PNG, JPG, JPEG, or TIFF files."
            }, status_code=400)
        
        # Read file content
        file_content = await file.read()
        
        # Check file size (Textract has limits)
        if len(file_content) > 10 * 1024 * 1024:  # 10MB limit
            return JSONResponse({
                "error": "File size too large. Please upload files smaller than 10MB."
            }, status_code=400)
        
        logger.info(f"Processing file: {file.filename} ({len(file_content)} bytes)")
        
        # Extract text using AWS Textract
        try:
            text = textract_service.extract_text_from_document(file_content)
            document_info = textract_service.get_document_info(file_content)
        except Exception as e:
            logger.error(f"Textract extraction failed: {e}")
            return JSONResponse({
                "error": f"Failed to extract text from document: {str(e)}"
            }, status_code=500)

        # Extract skills using the advanced skill extractor
        categorized_skills = skill_extractor.extract_skills_from_text(text)
        skill_summary = skill_extractor.get_skill_summary(categorized_skills)
        
        # Extract certifications using the certification extractor
        certification_results = certification_extractor.extract_certifications_from_text(text)

        return JSONResponse({
            "filename": file.filename,
            "content_length": len(text),
            "document_info": document_info,
            "skills": categorized_skills,
            "skills_summary": skill_summary,
            "certifications": certification_results['certifications'],
            "certification_details": certification_results['details'],
            "certifications_summary": certification_results['summary'],
            "extraction_method": "AWS Textract with advanced pattern matching"
        })
    except Exception as e:
        logger.error(f"Analysis failed: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)
