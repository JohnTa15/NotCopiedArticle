# NotCopiedArticle

<p align="center">
  <img src="https://img.shields.io/badge/Version-v1.5.0-blue?style=for-the-badge&logo=shield" alt="Version 1.5.0">
  <img src="https://img.shields.io/badge/Languages-English%20%7C%20Greek-purple?style=for-the-badge" alt="Languages">
  <img src="https://img.shields.io/badge/Python-3.13+-emerald?style=for-the-badge&logo=python" alt="Python">
  <img src="https://img.shields.io/badge/FastAPI-0.110+-009688?style=for-the-badge&logo=fastapi" alt="FastAPI">
</p>

**NotCopiedArticle** is an advanced Turnitin-style Academic Integrity, Plagiarism Checker, and Multilingual AI Content Detection Engine supporting **English (EN 🇬🇧)** and **Greek (EL 🇬🇷)** documents.

It provides dynamic vector-space similarity matching, statistical AI perplexity analysis, multi-page document parsing (PDF, DOCX, PPTX, ZIP), and a modern dark glassmorphism dashboard.

---

## 🌟 Key Features

### 1. 🔍 Smart Plagiarism & Similarity Engine
- **Winnowing MinHash Fingerprinting**: Hashing sliding windows ($k=4, w=4$) to select invariant hash min-points.
- **TF-IDF Vector Space Model**: Computes continuous Cosine Similarity ($\cos\theta$) between document passages and reference corpora.
- **Gestalt Pattern Matching**: Performs fuzzy sequence alignment to detect paraphrased or edited sentences.

### 2. 🧠 Statistical & Machine Learning AI Detector (EN / EL)
- **Perplexity & Shannon Entropy ($PP = 2^{H(X)}$)**: Evaluates vocabulary predictability and transition entropy across sentences.
- **Moving Average Type-Token Ratio (MATTR)**: Dynamically measures vocabulary richness without length bias.
- **Burstiness Index ($CV = \sigma / \mu$)**: Detects sentence length variance and structural rhythm differences between human and AI writing.
- **Stylometric Density Analysis**: Flags formal transitional markers and syntactic structures in both English and Greek.
- **Ensemble Probabilistic Classifier**: Outputs continuous AI confidence probabilities ($0.0\% - 100.0\%$).

### 3. 📦 Multi-Page & Archive Extraction
- **Supported Formats**: `.pdf`, `.docx`, `.doc`, `.pptx`, `.ppt`, `.txt`, `.md`, `.zip`.
- **Native ZIP Decompression**: Upload `.zip` archives to extract and scan all contained documents simultaneously.

### 4. 🎨 Dark Theme & Interactive Interface
- Modern glassmorphism UI with a multi-stage animated deep scan laser effect.
- Color-coded sentence highlighting (🔴 Red = Similarity Match, 🟣 Purple = AI Content).
- PDF Turnitin report export functionality.
- Live version indicator badge (`v1.3.0`) in the bottom-right corner.

---

## 🚀 Quick Start

### 1-Click Launchers
- **Windows**: Double-click `run.bat`
- **Linux / macOS**: Execute `./run.sh`

### Manual Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/JohnTa15/NotCopiedArticle.git
   cd NotCopiedArticle
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Launch the web application:
   ```bash
   python -m uvicorn app:app --host 127.0.0.1 --port 8000 --reload
   ```

4. Open your browser to `http://127.0.0.1:8000`.

---

## 📁 Repository Structure

```
NotCopiedArticle/
├── app.py                # FastAPI Web Server & REST API Endpoints
├── detector.py           # Winnowing, TF-IDF Cosine & AI Perplexity Engine
├── doc_parser.py         # Document Extractor (PDF, DOCX, PPTX, ZIP)
├── corpus.py             # Academic Knowledge Base Corpus
├── templates/
│   └── index.html        # Dark Mode Glassmorphism Dashboard UI
├── test_files/           # Sample test documents (.docx, .pptx, .zip)
├── run.bat               # Windows Launcher Script
├── run.sh                # Linux/macOS Launcher Script
├── VERSION               # Current Version Number (v1.3.0)
├── CHANGELOG.md          # Release History & Version Log
├── requirements.txt      # Python Dependencies
└── README.md             # Documentation
```

---

## 📜 License & Author

Developed by **JohnTa15**. Distributed under the MIT License.
