import pypdf
import docx
import pptx

def create_sample_files():
    # 1. Multi-page PDF
    writer = pypdf.PdfWriter()
    page1 = pypdf.PageObject.create_blank_page(width=612, height=792)
    writer.add_page(page1)
    
    with open("test_sample.pdf", "wb") as f:
        # Simple text PDF via reportlab or simple write
        pass

    # 2. Multi-paragraph Word docx
    doc = docx.Document()
    doc.add_heading('Academic Research on Artificial Intelligence in Higher Education', 0)
    doc.add_paragraph('Artificial intelligence is transforming higher education by personalizing learning paths and automating administrative tasks.')
    doc.add_paragraph('Furthermore, AI-driven assessment tools provide rapid feedback to students, enhancing learning outcomes.')
    doc.add_paragraph('Η τεχνητή νοημοσύνη διαδραματίζει κομβικό ρόλο στη σύγχρονη επιστημονική έρευνα. Επιπλέον, η ενσωμάτωση προηγμένων αλγορίθμων προσφέρει μια πολυδιάστατη προσέγγιση.')
    doc.save("test_paper.docx")

    # 3. Multi-slide PowerPoint pptx
    prs = pptx.Presentation()
    blank_slide_layout = prs.slide_layouts[6]
    
    slide1 = prs.slides.add_slide(blank_slide_layout)
    txBox = slide1.shapes.add_textbox(100, 100, 400, 200)
    tf = txBox.text_frame
    tf.text = "Climate Change and Coastal Ecosystem Resilience"
    
    slide2 = prs.slides.add_slide(blank_slide_layout)
    txBox2 = slide2.shapes.add_textbox(100, 100, 400, 200)
    tf2 = txBox2.text_frame
    tf2.text = "Coastal ecosystems play a crucial role in mitigating carbon emissions and protecting shorelines."

    prs.save("test_presentation.pptx")
    print("Created test_paper.docx and test_presentation.pptx successfully!")

if __name__ == "__main__":
    create_sample_files()
