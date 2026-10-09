"""
Reference Document Corpus for Plagiarism & Similarity Checking (English & Greek)
"""

from typing import List, Dict, Any

DEFAULT_CORPUS: List[Dict[str, Any]] = [
    {
        "id": "ref-en-001",
        "title": "Artificial Intelligence in Modern Education: Benefits and Challenges",
        "author": "Dr. Sarah Jenkins (Journal of Academic Technology, 2024)",
        "language": "en",
        "text": """Artificial intelligence is transforming higher education by personalizing learning paths and automating administrative tasks.
Furthermore, AI-driven assessment tools provide rapid feedback to students, enhancing learning outcomes.
However, academic integrity concerns have escalated with the widespread availability of large language models.
Educators must establish clear guidelines to ensure ethical usage while fostering critical thinking skills in students.
It is important to emphasize that AI should complement, not replace, human instruction and mentorship."""
    },
    {
        "id": "ref-en-002",
        "title": "Climate Change and Coastal Ecosystem Resilience",
        "author": "Prof. Mark Vance (Environmental Science Review, 2023)",
        "language": "en",
        "text": """Coastal ecosystems play a crucial role in mitigating carbon emissions and protecting shorelines from severe storm surges.
Rising ocean temperatures and sea level rise present severe threats to biodiversity in estuaries and coral reefs.
Restoration efforts must adopt a holistic approach, integrating traditional ecological knowledge with modern conservation strategies.
In conclusion, sustained international policy coordination is essential to preserve marine habitats for future generations."""
    },
    {
        "id": "ref-en-003",
        "title": "Quantum Computing Architectures and Cryptographic Protocols",
        "author": "Dr. Alan Turing Institute Research Group (2024)",
        "language": "en",
        "text": """Quantum computation leverages superposition and entanglement to solve complex mathematical problems at exponential speeds.
Post-quantum cryptography seeks to develop algorithms resistant to quantum cryptanalysis, such as lattice-based cryptography.
The transition to quantum-safe standards is a critical priority for cybersecurity infrastructure worldwide."""
    },
    {
        "id": "ref-el-001",
        "title": "Η Επίδραση της Τεχνητής Νοημοσύνης στην Εκπαίδευση",
        "author": "Δρ. Γεώργιος Παπαδόπουλος (Ελληνικό Περιοδικό Εκπαιδευτικής Τεχνολογίας, 2024)",
        "language": "el",
        "text": """Η τεχνητή νοημοσύνη αναδιαμορφώνει τη σύγχρονη εκπαιδευτική πραγματικότητα προσφέροντας προσαρμοσμένα μονοπάτια μάθησης.
Επιπλέον, τα συστήματα αυτά επιτρέπουν την αυτόματη αξιολόγηση και παρέχουν άμεση ανατροφοδότηση στους φοιτητές.
Αξίζει να σημειωθεί ότι η διατήρηση της ακαδημαϊκής ακεραιότητας αποτελεί πρόκληση με την εξάπλωση των μεγάλων γλωσσικών μοντέλων.
Είναι σημαντικό να αναφερθεί ότι η τεχνολογία πρέπει να λειτουργεί επικουρικά και όχι να αντικαταστήσει τον ανθρώπινο παράγοντα στη διδασκαλία.
Συμπερασματικά, απαιτείται ένα σαφές δεοντολογικό πλαίσιο για τη σωστή αξιοποίηση των εργαλείων AI."""
    },
    {
        "id": "ref-el-002",
        "title": "Κλιματική Αλλαγή και Προστασία του Παράκτιου Περιβάλλοντος στην Ελλάδα",
        "author": "Καθ. Ελένη Νικολάου (Περιβαλλοντικές Μελέτες, 2023)",
        "language": "el",
        "text": """Τα παράκτια οικοσυστήματα διαδραματίζουν κομβικό ρόλο στην απορρόφηση των εκπομπών άνθρακα και την προστασία από τη διάβρωση.
Η άνοδος της θερμοκρασίας της θάλασσας και η αλλαγή των καιρικών φαινομένων απειλούν τη βιοποικιλότητα στις ελληνικές ακτές.
Οι προσπάθειες αποκατάστασης πρέπει να βασίζονται σε μια ολιστική προσέγγιση που συνδυάζει την επιστημονική γνώση με την τοπική διαχείριση.
Κατά συνέπεια, η διακρατική συνεργασία είναι θεμελιώδους σημασίας για τη διατήρηση των θαλάσσιων πόρων."""
    },
    {
        "id": "ref-el-003",
        "title": "Φιλοσοφία και Δημοκρατία στην Αρχαία Αθήνα",
        "author": "Πανεπιστήμιο Αθηνών - Τομέας Φιλοσοφίας (2023)",
        "language": "el",
        "text": """Η αθηναϊκή δημοκρατία του πέμπτου αιώνα π.Χ. θεμελιώθηκε στις αρχές της ισηγορίας, της ισονομίας και της άμεσης συμμετοχής των πολιτών.
Ο Σωκράτης και ο Πλάτων αμφισβήτησαν τα ρητορικά σχήματα των σοφιστών, προτείνοντας τη διαλεκτική μέθοδο για την αναζήτηση της αλήθειας.
Η πολιτική φιλοσοφία της κλασικής εποχής συνεχίζει να αποτελεί σημείο αναφοράς για τους σύγχρονους δημοκρατικούς θεσμούς."""
    }
]

class CorpusManager:
    def __init__(self):
        self.documents = list(DEFAULT_CORPUS)

    def get_all(self) -> List[Dict[str, Any]]:
        return self.documents

    def add_document(self, title: str, author: str, text: str, language: str = None) -> Dict[str, Any]:
        doc_id = f"ref-user-{len(self.documents) + 1:03d}"
        doc = {
            "id": doc_id,
            "title": title,
            "author": author,
            "language": language or "en",
            "text": text
        }
        self.documents.append(doc)
        return doc

corpus_inst = CorpusManager()
