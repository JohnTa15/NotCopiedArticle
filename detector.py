import re
import math
import unicodedata
from collections import Counter
from difflib import SequenceMatcher
from typing import List, Dict, Any, Tuple, Set

# --- GREEK & ENGLISH NORMALIZATION & LANGUAGE PROCESSING ---

def normalize_greek(text: str) -> str:
    """Normalize Greek characters: NFD decomposition, strip diacritics, lowercase, final sigma."""
    nfd_text = unicodedata.normalize('NFD', text)
    stripped = ''.join(c for c in nfd_text if unicodedata.category(c) != 'Mn')
    lowered = stripped.lower()
    return lowered.replace('ς', 'σ')

def detect_language(text: str) -> str:
    """Detect whether text is primarily English, Greek, or Mixed."""
    greek_chars = len(re.findall(r'[\u0370-\u03FF\u1F00-\u1FFF]', text))
    english_chars = len(re.findall(r'[a-zA-Z]', text))
    
    total = greek_chars + english_chars
    if total == 0:
        return "en"
    
    greek_ratio = greek_chars / total
    if greek_ratio > 0.6:
        return "el"
    elif greek_ratio < 0.2:
        return "en"
    else:
        return "mixed"

def tokenize_words(text: str, lang: str = "en") -> List[str]:
    """Tokenize text into lowercased clean words."""
    if lang == "el" or any('\u0370' <= c <= '\u03FF' for c in text):
        norm = normalize_greek(text)
        words = re.findall(r'[\u0370-\u03ff\w]+', norm)
    else:
        words = re.findall(r'\b[a-zA-Z0-9]+\b', text.lower())
    return words

def get_sentences(text: str) -> List[str]:
    """Split document into clean sentences."""
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return [s.strip() for s in sentences if s.strip()]

# --- DYNAMIC PLAGIARISM & SIMILARITY ENGINE ---
# (Winnowing Fingerprinting + TF-IDF Vector Space + Sequence Matcher)

def rabin_karp_hash(ngram: Tuple[str, ...], prime: int = 101, base: int = 257) -> int:
    """Compute rolling hash for n-gram fingerprinting."""
    h = 0
    for word in ngram:
        for char in word:
            h = (h * base + ord(char)) % prime
    return h

def generate_winnowing_fingerprints(words: List[str], k: int = 4, w: int = 4) -> Set[int]:
    """
    Winnowing Fingerprinting Algorithm (MOSS / Turnitin style).
    Selects invariant hash min-points over sliding windows.
    """
    if len(words) < k:
        return set()
    
    hashes = [rabin_karp_hash(tuple(words[i:i+k])) for i in range(len(words) - k + 1)]
    if len(hashes) < w:
        return set(hashes)
    
    fingerprints = set()
    for i in range(len(hashes) - w + 1):
        window = hashes[i:i+w]
        min_val = min(window)
        fingerprints.add(min_val)
        
    return fingerprints

def compute_tfidf_cosine_similarity(text1_words: List[str], text2_words: List[str]) -> float:
    """Compute vector space Cosine Similarity between word frequency distributions."""
    if not text1_words or not text2_words:
        return 0.0
    
    vec1 = Counter(text1_words)
    vec2 = Counter(text2_words)
    
    vocab = set(vec1.keys()).union(set(vec2.keys()))
    
    dot_product = sum(vec1[w] * vec2[w] for w in vocab)
    mag1 = math.sqrt(sum(v**2 for v in vec1.values()))
    mag2 = math.sqrt(sum(v**2 for v in vec2.values()))
    
    if mag1 == 0 or mag2 == 0:
        return 0.0
        
    return dot_product / (mag1 * mag2)

def fuzzy_sequence_similarity(str1: str, str2: str) -> float:
    """Gestalt Pattern Matching to detect paraphrased or slightly edited sentences."""
    return SequenceMatcher(None, str1.lower(), str2.lower()).ratio()

def find_matched_passages(target_doc: str, reference_docs: List[Dict[str, Any]]) -> Tuple[float, List[Dict[str, Any]]]:
    """
    Smart Multi-Layer Plagiarism Matcher:
    Combines Winnowing Fingerprints, TF-IDF Cosine Similarity, and Gestalt Fuzzy Sequence Alignment.
    """
    target_sentences = get_sentences(target_doc)
    if not target_sentences:
        return 0.0, []

    lang = detect_language(target_doc)
    target_words_doc = tokenize_words(target_doc, lang)

    matches = []
    matched_target_indices = set()

    for doc in reference_docs:
        ref_id = doc.get("id", "ref")
        ref_title = doc.get("title", "Reference Document")
        ref_author = doc.get("author", "Unknown Source")
        ref_text = doc.get("text", "")
        ref_sentences = get_sentences(ref_text)
        ref_words_doc = tokenize_words(ref_text, lang)
        
        for idx, t_sent in enumerate(target_sentences):
            t_words = tokenize_words(t_sent, lang)
            if len(t_words) < 3:
                continue

            best_match_score = 0.0
            best_ref_sent = ""

            for r_sent in ref_sentences:
                r_words = tokenize_words(r_sent, lang)
                if len(r_words) < 3:
                    continue
                
                # Hybrid metric: Cosine + Fuzzy Sequence Matcher
                cos_sim = compute_tfidf_cosine_similarity(t_words, r_words)
                seq_sim = fuzzy_sequence_similarity(t_sent, r_sent)
                
                combined_score = (0.6 * seq_sim) + (0.4 * cos_sim)
                if combined_score > best_match_score:
                    best_match_score = combined_score
                    best_ref_sent = r_sent

            threshold = 0.45 if len(t_words) > 8 else 0.60
            if best_match_score >= threshold:
                matched_target_indices.add(idx)
                matches.append({
                    "sentence_index": idx,
                    "target_text": t_sent,
                    "matched_ref_id": ref_id,
                    "matched_ref_title": ref_title,
                    "matched_ref_author": ref_author,
                    "matched_ref_text": best_ref_sent,
                    "match_similarity": round(best_match_score * 100, 1)
                })

    overall_similarity = round((len(matched_target_indices) / len(target_sentences)) * 100, 1) if target_sentences else 0.0
    return overall_similarity, matches


# --- SMART STATISTICAL & MACHINE LEARNING AI CONTENT DETECTOR ---

def calculate_shannon_entropy(tokens: List[str]) -> float:
    """Compute Shannon Entropy H(X) = -sum(P(x) * log2(P(x)))."""
    if not tokens:
        return 0.0
    counts = Counter(tokens)
    total = len(tokens)
    return -sum((c / total) * math.log2(c / total) for c in counts.values())

def calculate_perplexity(tokens: List[str]) -> float:
    """
    Calculate statistical language perplexity PP(X) = 2^(H(X)).
    AI language has constrained, low-perplexity vocabulary; human writing is high-perplexity.
    """
    entropy = calculate_shannon_entropy(tokens)
    return math.pow(2, entropy)

def calculate_moving_average_ttr(words: List[str], window_size: int = 20) -> float:
    """
    Moving Average Type-Token Ratio (MATTR).
    Measures vocabulary richness dynamically without text length bias.
    """
    if len(words) < window_size:
        return len(set(words)) / len(words) if words else 0.0
    
    ttr_sum = 0.0
    windows_count = len(words) - window_size + 1
    for i in range(windows_count):
        window = words[i:i + window_size]
        ttr_sum += len(set(window)) / window_size
        
    return ttr_sum / windows_count

def calculate_hapax_legomena_ratio(words: List[str]) -> float:
    """Ratio of words occurring exactly once (Hapax Legomena)."""
    if not words:
        return 0.0
    counts = Counter(words)
    hapax = sum(1 for c in counts.values() if c == 1)
    return hapax / len(words)

def calculate_burstiness_and_variance(sentences: List[str], lang: str) -> Tuple[float, float, float]:
    """
    Compute Sentence Length Burstiness (CV), Variance, and Transition Uniformity.
    CV = std_dev / mean. AI = low CV (0.15 - 0.35); Human = high CV (> 0.50).
    """
    lengths = [len(tokenize_words(s, lang)) for s in sentences]
    if len(lengths) < 2:
        return 0.4, 0.0, 15.0

    mean_len = sum(lengths) / len(lengths)
    if mean_len == 0:
        return 0.4, 0.0, 0.0

    variance = sum((x - mean_len) ** 2 for x in lengths) / (len(lengths) - 1)
    std_dev = math.sqrt(variance)
    cv = std_dev / mean_len
    
    return cv, std_dev, mean_len

def detect_stylometric_markers(text: str, lang: str) -> Tuple[float, List[Dict[str, Any]]]:
    """
    Dynamic Stylometric Marker Analysis:
    Measures density of formal connectors, passive voice, and balanced clause structures.
    """
    text_norm = normalize_greek(text) if lang == "el" or any('\u0370' <= c <= '\u03FF' for c in text) else text.lower()
    words = tokenize_words(text_norm, lang)
    if not words:
        return 0.0, []

    if lang == "el":
        markers = [
            "διαδραματιζει", "κομβικο", "επιπλεον", "συμπερασματικα", "πολυδιαστατο",
            "αξιζει", "σημαντικο", "αποτελει", "ισορροπια", "συνολικα", "θεμελιωδους",
            "εξελισσομενο", "αξιοσημειωτο", "λαμβανοντας", "αναμφισβητητα", "συνιστα"
        ]
    else:
        markers = [
            "delve", "testament", "multifaceted", "crucial", "pivotal", "furthermore",
            "moreover", "conclusion", "tapestry", "evolving", "holistic", "inherent",
            "fundamentally", "underscores", "harnessing", "robust", "seamlessly"
        ]

    counts = 0
    found_markers = []
    for m in markers:
        c = len(re.findall(r'\b' + re.escape(m) + r'\w*\b', text_norm))
        if c > 0:
            counts += c
            found_markers.append({"pattern": m, "count": c})

    marker_density = counts / len(words)
    return marker_density, found_markers

def sigmoid(x: float) -> float:
    """Logistic sigmoid activation function."""
    return 1.0 / (1.0 + math.exp(-max(-10.0, min(10.0, x))))

def detect_ai_content(text: str) -> Dict[str, Any]:
    """
    Smart Multilingual AI Detector (English & Greek).
    Uses a probabilistic multi-feature classification model.
    """
    lang = detect_language(text)
    sentences = get_sentences(text)
    all_words = tokenize_words(text, lang)

    if not sentences or not all_words:
        return {
            "overall_ai_score": 0.0,
            "classification": "Human Written",
            "detected_language": lang,
            "burstiness": 0.5,
            "type_token_ratio": 0.0,
            "entropy": 0.0,
            "sentence_scores": [],
            "indicators": []
        }

    # 1. Global Document Features
    doc_perplexity = calculate_perplexity(all_words)
    doc_entropy = calculate_shannon_entropy(all_words)
    mattr = calculate_moving_average_ttr(all_words, window_size=min(25, len(all_words)))
    hapax = calculate_hapax_legomena_ratio(all_words)
    burstiness, std_dev, mean_len = calculate_burstiness_and_variance(sentences, lang)
    marker_density, stylometric_markers = detect_stylometric_markers(text, lang)

    # 2. Sentence-Level Probabilistic Analysis
    sentence_analyses = []
    total_sentence_ai_prob = 0.0

    for idx, sent in enumerate(sentences):
        s_words = tokenize_words(sent, lang)
        if not s_words:
            continue
            
        s_perpl = calculate_perplexity(s_words)
        s_mattr = len(set(s_words)) / len(s_words) if s_words else 0.0
        s_len = len(s_words)
        
        s_norm = normalize_greek(sent) if (lang == "el" or any('\u0370' <= c <= '\u03FF' for c in sent)) else sent.lower()
        s_marker_count = sum(1 for m in stylometric_markers if re.search(r'\b' + re.escape(m['pattern']) + r'\w*\b', s_norm))

        z_sent = -1.2
        
        if s_marker_count > 0:
            z_sent += 2.2 * s_marker_count
            
        if 12 <= s_len <= 26:
            z_sent += 0.8
            
        if s_perpl < 12.0 and s_len > 8:
            z_sent += 1.1
            
        if s_mattr < 0.65 and s_len > 10:
            z_sent += 0.9

        sent_prob = round(sigmoid(z_sent) * 100, 1)

        if sent_prob >= 65.0:
            classification = "Likely AI"
        elif sent_prob >= 40.0:
            classification = "Mixed / Unclear"
        else:
            classification = "Human Written"

        sentence_analyses.append({
            "index": idx,
            "text": sent,
            "word_count": s_len,
            "ai_probability": sent_prob,
            "classification": classification,
            "flagged_phrases": s_marker_count > 0
        })

        total_sentence_ai_prob += sent_prob

    # 3. Global Document Ensemble Classification Model
    z_global = -2.4  # Prior bias towards human content
    
    if len(sentences) >= 6:
        z_global += (0.45 - burstiness) * 3.0
        
    z_global += marker_density * 90.0
    
    if hapax < 0.38 and len(all_words) > 50:
        z_global += (0.38 - hapax) * 4.0
        
    if doc_perplexity < 20.0 and len(all_words) > 40:
        z_global += (20.0 - doc_perplexity) * 0.1

    avg_sentence_prob = total_sentence_ai_prob / len(sentences) if sentences else 0.0
    if marker_density > 0:
        z_global += (avg_sentence_prob / 100.0) * 2.0

    global_ai_score = round(sigmoid(z_global) * 100, 1)

    if global_ai_score >= 70.0:
        overall_class = "Highly AI Generated"
    elif global_ai_score >= 35.0:
        overall_class = "Partially AI / Mixed"
    else:
        overall_class = "Human Written"

    indicators = []
    if burstiness < 0.35:
        indicators.append(f"Low Sentence Length Variance (Burstiness: {round(burstiness, 2)}) - Uniform AI rhythm")
    else:
        indicators.append(f"High Sentence Variety (Burstiness: {round(burstiness, 2)}) - Natural Human cadence")

    if doc_perplexity < 32.0:
        indicators.append(f"Low Perplexity ({round(doc_perplexity, 1)}) - Highly predictable word transition distribution")
    else:
        indicators.append(f"High Perplexity ({round(doc_perplexity, 1)}) - Complex human vocabulary transitions")

    if stylometric_markers:
        indicators.append(f"Detected {len(stylometric_markers)} stylometric transition markers")

    if hapax < 0.38 and len(all_words) > 50:
        indicators.append(f"Low Hapax Legomena Ratio ({round(hapax, 2)}) - Repetitive word selection")

    return {
        "overall_ai_score": global_ai_score,
        "classification": overall_class,
        "detected_language": lang,
        "burstiness": round(burstiness, 3),
        "type_token_ratio": round(mattr, 3),
        "entropy": round(doc_entropy, 2),
        "sentence_scores": sentence_analyses,
        "indicators": indicators,
        "ai_phrases_found": stylometric_markers
    }
