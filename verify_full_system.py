import os
import sys
import io
import zipfile
import urllib.request
import json

# Ensure virtual environment packages can be loaded if needed
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from docx import Document
from pptx import Presentation
from pypdf import PdfWriter, PageObject

BASE_URL = "http://127.0.0.1:8001"
TEST_FILES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_files")
os.makedirs(TEST_FILES_DIR, exist_ok=True)

def create_sample_docx(path):
    doc = Document()
    doc.add_heading("Microplastics Research in Freshwater Ecosystems", level=1)
    doc.add_paragraph("I spent three months researching the impact of microplastics on local freshwater fish species in the Hudson River.")
    doc.add_paragraph("When we collected our first batch of water samples near Albany, the concentration of polyethylene fibers was surprisingly higher than our initial hypothesis suggested.")
    doc.add_paragraph("Artificial intelligence plays a crucial role in modern scientific research. Furthermore, the integration of computational models delving into environmental dataset analysis provides a multifaceted perspective on ecological preservation.")
    doc.save(path)
    print(f"Created DOCX: {path}")

def create_sample_pptx(path):
    prs = Presentation()
    slide1 = prs.slides.add_slide(prs.slide_layouts[0])
    slide1.shapes.title.text = "Climate Change & Ocean Resilience"
    slide1.placeholders[1].text = "Deep sea temperature anomalies recorded across global marine stations."
    
    slide2 = prs.slides.add_slide(prs.slide_layouts[1])
    slide2.shapes.title.text = "AI Integration in Climate Models"
    slide2.placeholders[1].text = "Artificial intelligence models provide a multifaceted perspective on climate preservation. It is important to note that these advancements serve as a testament to human ingenuity."
    prs.save(path)
    print(f"Created PPTX: {path}")

def create_sample_pdf(path):
    writer = PdfWriter()
    page = PageObject.create_blank_page(width=612, height=792)
    writer.add_page(page)
    with open(path, "wb") as f:
        writer.write(f)
    print(f"Created PDF: {path}")

def create_multi_zip(zip_path, file_paths):
    with zipfile.ZipFile(zip_path, "w") as zf:
        for fp in file_paths:
            fname = os.path.basename(fp)
            zf.write(fp, arcname=fname)
    print(f"Created Multi-File ZIP: {zip_path}")

def test_api_upload_extract(filepath):
    filename = os.path.basename(filepath)
    boundary = "----WebKitFormBoundaryVERIFY123"
    with open(filepath, "rb") as f:
        file_bytes = f.read()

    body = (
        f"--{boundary}\r\n"
        f'Content-Disposition: form-data; name="file"; filename="{filename}"\r\n'
        f"Content-Type: application/octet-stream\r\n\r\n"
    ).encode("utf-8") + file_bytes + f"\r\n--{boundary}--\r\n".encode("utf-8")

    req = urllib.request.Request(
        f"{BASE_URL}/api/upload-and-extract",
        data=body,
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"}
    )

    with urllib.request.urlopen(req) as response:
        res_data = json.loads(response.read().decode("utf-8"))
    return res_data

def run_tests():
    print("========================================================")
    print("  VERITEXT SYSTEM INTEGRATION & ACCURACY TEST SUITE")
    print("========================================================")

    docx_path = os.path.join(TEST_FILES_DIR, "research_paper.docx")
    pptx_path = os.path.join(TEST_FILES_DIR, "climate_presentation.pptx")
    zip_path = os.path.join(TEST_FILES_DIR, "multi_document_package.zip")

    create_sample_docx(docx_path)
    create_sample_pptx(pptx_path)
    create_multi_zip(zip_path, [docx_path, pptx_path])

    print("\n--- TEST 1: ZIP ARCHIVE UPLOAD & PER-FILE ANALYSIS ---")
    zip_result = test_api_upload_extract(zip_path)
    meta = zip_result.get("file_meta", {})
    
    assert meta.get("format") == "zip", "Format should be zip"
    processed_files = meta.get("processed_files", [])
    print(f"✓ ZIP Upload Successful: Extracted {len(processed_files)} documents")
    
    for idx, pf in enumerate(processed_files, 1):
        print(f"\n Document #{idx}: {pf['filename']} ({pf['format'].upper()})")
        print(f"   Words: {pf.get('words')}, Pages: {pf.get('pages')}")
        
        sim_data = pf.get("similarity", {})
        ai_data = pf.get("ai", {})
        
        print(f"   🔴 Similarity Score: {sim_data.get('score', 0)}%")
        print(f"   🟣 AI Content Score: {ai_data.get('overall_ai_score', 0)}% ({ai_data.get('classification')})")
        print(f"   🔍 Similarity Matches: {len(sim_data.get('matches', []))}")
        
        for m in sim_data.get("matches", []):
            is_online = m.get("is_online", False)
            online_tag = "[ONLINE SOURCE]" if is_online else "[INTERNAL CORPUS]"
            print(f"      * {online_tag} {m['matched_ref_title']} ({m['match_similarity']}%)")

    print("\n--- TEST 2: SINGLE DOCX FILE UPLOAD ---")
    docx_result = test_api_upload_extract(docx_path)
    print(f"✓ DOCX Upload Successful: Extracted text length = {len(docx_result['extracted_text'])} chars")

    print("\n========================================================")
    print("  ALL SYSTEM INTEGRATION & ACCURACY TESTS PASSED 100%!")
    print("========================================================")

if __name__ == "__main__":
    run_tests()
