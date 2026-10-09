import json
from detector import detect_ai_content, find_matched_passages, detect_language
from corpus import corpus_inst
from app import SAMPLE_TEXTS

def run_tests():
    print("=== RUNNING DETECTOR TESTS (ENGLISH & GREEK) ===")
    
    for key, text in SAMPLE_TEXTS.items():
        lang = detect_language(text)
        ai_res = detect_ai_content(text)
        sim_score, matches = find_matched_passages(text, corpus_inst.get_all())
        
        print(f"\nSample: [{key.upper()}] | Detected Lang: {lang.upper()}")
        print(f"  - AI Score: {ai_res['overall_ai_score']}% ({ai_res['classification']})")
        print(f"  - Burstiness: {ai_res['burstiness']} | TTR: {ai_res['type_token_ratio']}")
        print(f"  - Similarity Score: {sim_score}% | Matches: {len(matches)}")
        if matches:
            for m in matches:
                print(f"    * Matched Source: {m['matched_ref_title']} ({m['match_similarity']}%)")
                
    print("\n=== ALL TESTS COMPLETED SUCCESSFULLY ===")

if __name__ == "__main__":
    run_tests()
