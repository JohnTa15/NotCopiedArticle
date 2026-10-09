import os
import zipfile
import urllib.request
import json

test_dir = "C:/Users/JohnJohn/NotCopiedArticle/test_files"
zip_path = os.path.join(test_dir, "academic_submission.zip")

# Package sample_paper.docx and sample_presentation.pptx into zip
with zipfile.ZipFile(zip_path, 'w') as zf:
    zf.write(os.path.join(test_dir, "sample_paper.docx"), arcname="paper_section.docx")
    zf.write(os.path.join(test_dir, "sample_presentation.pptx"), arcname="presentation_section.pptx")

print(f"Created ZIP archive at {zip_path}")

# Test API Upload
url = 'http://127.0.0.1:8000/api/upload-and-analyze'
boundary = '----WebKitFormBoundaryZIP7MA4YWxkTrZu0gW'

with open(zip_path, 'rb') as f:
    zip_bytes = f.read()

body = (
    f'--{boundary}\r\n'
    f'Content-Disposition: form-data; name="file"; filename="academic_submission.zip"\r\n'
    f'Content-Type: application/zip\r\n\r\n'
).encode('utf-8') + zip_bytes + f'\r\n--{boundary}--\r\n'.encode('utf-8')

req = urllib.request.Request(url, data=body, headers={
    'Content-Type': f'multipart/form-data; boundary={boundary}'
})

res = urllib.request.urlopen(req)
result = json.loads(res.read().decode('utf-8'))

print("\n=== ZIP UPLOAD TEST SUCCESSFUL ===")
print("File Meta:", result.get("file_meta"))
print("Extracted Text Preview:\n", result.get("extracted_text")[:300])
print("Similarity Score:", result["similarity"]["score"], "%")
print("AI Score:", result["ai"]["overall_ai_score"], "%")
