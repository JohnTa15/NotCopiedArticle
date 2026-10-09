import os
import uvicorn
from fastapi import FastAPI, HTTPException, Request, UploadFile, File
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

from detector import detect_language, get_sentences, tokenize_words, find_matched_passages, detect_ai_content
from corpus import corpus_inst
from doc_parser import parse_uploaded_file

app = FastAPI(
    title="Turnitin AI & Similarity Detector",
    description="Academic Integrity & AI Detector supporting English & Greek",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    text: str

class AddSourceRequest(BaseModel):
    title: str
    author: Optional[str] = "Unknown"
    text: str

SAMPLE_TEXTS = {
    "en_human": (
        "I spent three months researching the impact of microplastics on local freshwater fish species in the Hudson River. "
        "When we collected our first batch of water samples near Albany, the concentration of polyethylene fibers was surprisingly higher than our initial hypothesis suggested. "
        "Fieldwork wasn't easy—rainy mornings and broken water samplers slowed us down. "
        "But analyzing the gills under the microscope revealed clear particle blockages, proving that microplastic pollution is actively affecting aquatic respiration in upstate New York."
    ),
    "en_ai": (
        "Artificial intelligence plays a crucial role in modern scientific research. "
        "Furthermore, the integration of computational models delving into environmental dataset analysis provides a multifaceted perspective on ecological preservation. "
        "It is important to note that these advancements serve as a testament to human ingenuity. "
        "In conclusion, adopting a holistic approach towards technology harnessing will seamlessly transform how we address climate change."
    ),
    "el_human": (
        "Κατά τη διάρκεια της τριμηνιαίας έρευνάς μας στο πεδίο, εξετάσαμε την παρουσία μικροπλαστικών στα ψάρια του Θερμαϊκού Κόλπου. "
        "Η συλλογή των δειγμάτων έγινε κάτω από δύσκολες καιρικές συνθήκες κοντά στην εκβολή του Αξιού. "
        "Παρά τις τεχνικές δυσκολίες με τις δίχτυες βυθού, η εργαστηριακή ανάλυση έδειξε σοβαρή συσσώρευση σωματιδίων στους ιστούς, επιβεβαιώνοντας τις υποψίες μας για την τοπική μόλυνση."
    ),
    "el_ai": (
        "Η τεχνητή νοημοσύνη διαδραματίζει κομβικό ρόλο στη σύγχρονη επιστημονική έρευνα. "
        "Επιπλέον, η ενσωμάτωση προηγμένων αλγορίθμων προσφέρει μια πολυδιάστατη προσέγγιση στην ανάλυση δεδομένων. "
        "Είναι σημαντικό να αναφερθεί ότι οι τεχνολογικές αυτές εξελίξεις αποτελούν ζωντανό παράδειγμα της ανθρώπινης προόδου. "
        "Συμπερασματικά, η υιοθέτηση μιας ευαίσθητης ισορροπίας μεταξύ καινοτομίας και δεοντολογίας θα διαμορφώσει θετικά το μέλλον της κοινωνίας."
    ),
    "plagiarism_test": (
        "Artificial intelligence is transforming higher education by personalizing learning paths and automating administrative tasks. "
        "Furthermore, AI-driven assessment tools provide rapid feedback to students, enhancing learning outcomes. "
        "Η τεχνητή νοημοσύνη αναδιαμορφώνει τη σύγχρονη εκπαιδευτική πραγματικότητα προσφέροντας προσαρμοσμένα μονοπάτια μάθησης. "
        "Επιπλέον, τα συστήματα αυτά επιτρέπουν την αυτόματη αξιολόγηση και παρέχουν άμεση ανατροφοδότηση στους φοιτητές."
    )
}

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    template_path = os.path.join(os.path.dirname(__file__), "templates", "index.html")
    if not os.path.exists(template_path):
        raise HTTPException(status_code=404, detail="Template not found")
    with open(template_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

@app.get("/api/samples")
async def get_samples():
    return JSONResponse(content=SAMPLE_TEXTS)

@app.post("/api/add-reference")
async def add_reference(req: AddSourceRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    lang = detect_language(req.text)
    doc = corpus_inst.add_document(title=req.title, author=req.author, text=req.text, language=lang)
    return JSONResponse(content=doc)

@app.post("/api/analyze")
async def analyze_document(req: AnalyzeRequest):
    text = req.text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text cannot be empty")
        
    detected_lang = detect_language(text)
    sentences = get_sentences(text)
    words = tokenize_words(text, detected_lang)
    
    # 1. Similarity Engine
    reference_corpus = corpus_inst.get_all()
    similarity_score, matches = find_matched_passages(text, reference_corpus)
    
    # 2. AI Content Detector Engine
    ai_result = detect_ai_content(text)
    
    return JSONResponse(content={
        "language": detected_lang,
        "extracted_text": text,
        "stats": {
            "words": len(words),
            "characters": len(text),
            "sentences": len(sentences)
        },
        "similarity": {
            "score": similarity_score,
            "matches": matches
        },
        "ai": ai_result
    })

@app.post("/api/upload-and-extract")
async def upload_and_extract(file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()
        extracted_text, file_meta = parse_uploaded_file(file.filename or "document.txt", file_bytes)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to extract document text: {str(e)}")
        
    text = extracted_text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Document contains no readable text")

    # If ZIP archive, run per-document similarity and AI analysis for each extracted file
    if file_meta.get("format") == "zip" and "processed_files" in file_meta:
        reference_corpus = corpus_inst.get_all()
        for pfile in file_meta["processed_files"]:
            ptext = pfile.get("text", "").strip()
            if ptext:
                plang = detect_language(ptext)
                psim_score, pmatches = find_matched_passages(ptext, reference_corpus)
                pai_result = detect_ai_content(ptext)
                pfile["similarity"] = {
                    "score": psim_score,
                    "matches": pmatches
                }
                pfile["ai"] = pai_result

    return JSONResponse(content={
        "filename": file.filename,
        "file_meta": file_meta,
        "extracted_text": text
    })

@app.post("/api/upload-and-analyze")
async def upload_and_analyze(file: UploadFile = File(...)):
    try:
        file_bytes = await file.read()
        extracted_text, file_meta = parse_uploaded_file(file.filename or "document.txt", file_bytes)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to extract document text: {str(e)}")
        
    text = extracted_text.strip()
    if not text:
        raise HTTPException(status_code=400, detail="Document contains no readable text")

    reference_corpus = corpus_inst.get_all()

    # If ZIP archive, run per-document similarity and AI analysis for each extracted file
    if file_meta.get("format") == "zip" and "processed_files" in file_meta:
        for pfile in file_meta["processed_files"]:
            ptext = pfile.get("text", "").strip()
            if ptext:
                plang = detect_language(ptext)
                psim_score, pmatches = find_matched_passages(ptext, reference_corpus)
                pai_result = detect_ai_content(ptext)
                pfile["similarity"] = {
                    "score": psim_score,
                    "matches": pmatches
                }
                pfile["ai"] = pai_result

    detected_lang = detect_language(text)
    sentences = get_sentences(text)
    words = tokenize_words(text, detected_lang)
    
    # 1. Similarity Engine
    similarity_score, matches = find_matched_passages(text, reference_corpus)
    
    # 2. AI Content Detector Engine
    ai_result = detect_ai_content(text)
    
    return JSONResponse(content={
        "filename": file.filename,
        "file_meta": file_meta,
        "language": detected_lang,
        "extracted_text": text,
        "stats": {
            "words": len(words),
            "characters": len(text),
            "sentences": len(sentences)
        },
        "similarity": {
            "score": similarity_score,
            "matches": matches
        },
        "ai": ai_result
    })

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
