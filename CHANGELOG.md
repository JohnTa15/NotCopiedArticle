# VeriText AI & Plagiarism Detector Changelog

## [v1.4.0] - 2026-10-09
### Added
- **Selective Document Picker & Checkbox Drawer**: Allows selecting specific files (one, several, or all) from multi-document packages or `.zip` archives.
- **Isolated File Preview Modal**: Click `👁️ Preview` on any extracted document to view its text in a clean modal without endless scrolling.
- **Targeted Scan Execution**: Execute similarity & AI detection specifically on selected document subsets.
- **Version Badge**: Updated bottom-right badge to `v1.4.0`.

## [v1.3.0] - 2026-10-09
### Added
- **ZIP Archive Support**: Native decompression and extraction of `.zip` files containing `.pdf`, `.pptx`, `.docx`, `.doc`, `.txt`, `.md` documents.
- **Version Indicator**: Displayed `v1.3.0` release badge in the bottom-right corner of the dashboard.
- **Smart Dynamic NLP Engine**: Replaced static conditions with Winnowing MinHash, TF-IDF Cosine Similarity, Perplexity entropy, MATTR vocabulary richness, and Burstiness variance for both English 🇬🇧 and Greek 🇬🇷.
- **Dark Mode & Animations**: Glassmorphism dark UI with multi-stage animated deep scan laser progress sequence.
- **Script Automation**: Created `run.bat` (Windows) and `run.sh` (Linux/macOS) single-click execution scripts.
