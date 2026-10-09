import os
import pypdf
import docx
import pptx

test_dir = "C:/Users/JohnJohn/turnitin_ai_detector/test_files"
os.makedirs(test_dir, exist_ok=True)

# 1. Create a 3-page PDF file using pypdf
writer = pypdf.PdfWriter()
page1_text = "Page 1: Artificial intelligence is transforming higher education by personalizing learning paths and automating administrative tasks. Furthermore, AI-driven assessment tools provide rapid feedback."
page2_text = "Page 2: Η τεχνητή νοημοσύνη διαδραματίζει κομβικό ρόλο στη σύγχρονη επιστημονική έρευνα. Επιπλέον, η ενσωμάτωση προηγμένων αλγορίθμων προσφέρει μια πολυδιάστατη προσέγγιση."
page3_text = "Page 3: Fieldwork in environmental science requires rigorous sampling methodology to evaluate microplastic pollution across river basins."

# Create test files
print("Creating DOCX & PPTX files...")

# 2. Create DOCX
doc = docx.Document()
doc.add_heading('Academic Research Paper', 0)
doc.add_paragraph('This is paragraph 1. Microplastics in freshwater fish species are an emerging environmental hazard in the Hudson River basin.')
doc.add_paragraph('Furthermore, the integration of computational models delving into dataset analysis provides a multifaceted perspective on ecological preservation.')
table = doc.add_table(rows=2, cols=2)
table.cell(0, 0).text = 'Sample ID'
table.cell(0, 1).text = 'Concentration'
table.cell(1, 0).text = 'HD-001'
table.cell(1, 1).text = '45.2 mg/L'
doc.save(os.path.join(test_dir, "sample_paper.docx"))

# 3. Create PPTX (3 slides)
prs = pptx.Presentation()
slide1 = prs.slides.add_slide(prs.slide_layouts[0])
slide1.shapes.title.text = "Slide 1: Climate Change & Ocean Resiliency"
slide1.placeholders[1].text = "Coastal ecosystems play a crucial role in mitigating carbon emissions."

slide2 = prs.slides.add_slide(prs.slide_layouts[1])
slide2.shapes.title.text = "Slide 2: Η Επίδραση της Τεχνητής Νοημοσύνης"
slide2.placeholders[1].text = "Αξίζει να σημειωθεί ότι η διατήρηση της ακαδημαϊκής ακεραιότητας αποτελεί πρόκληση."

slide3 = prs.slides.add_slide(prs.slide_layouts[1])
slide3.shapes.title.text = "Slide 3: Conclusion & Next Steps"
slide3.placeholders[1].text = "International policy coordination is essential to preserve marine habitats."
prs.save(os.path.join(test_dir, "sample_presentation.pptx"))

print(f"Generated test files in {test_dir}")
