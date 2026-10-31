"""Pure eligibility rules and TF-IDF recommendations; no fabricated eligibility."""
from datetime import date

SUPPORTED = {"age_min", "age_max", "income_max", "states", "occupations"}

def evaluate(profile, rules):
    checks = []
    for key, expected in rules.items():
        if key not in SUPPORTED:
            checks.append({"field": key, "result": "unknown", "reason": "Unsupported rule; manual verification required"})
            continue
        source_field = {"age_min":"age", "age_max":"age", "income_max":"annual_income", "states":"state", "occupations":"occupation"}[key]
        actual = profile.get(source_field)
        if actual is None or actual == "":
            checks.append({"field":key,"result":"unknown","reason":f"Missing {source_field}"})
            continue
        try:
            if key == "age_min": ok = float(actual) >= float(expected)
            elif key == "age_max": ok = float(actual) <= float(expected)
            elif key == "income_max": ok = float(actual) <= float(expected)
            elif key == "states": ok = str(actual).strip().lower() in {str(x).strip().lower() for x in expected}
            else: ok = str(actual).strip().lower() in {str(x).strip().lower() for x in expected}
            checks.append({"field":key,"result":"pass" if ok else "fail","actual":actual,"expected":expected})
        except (TypeError, ValueError):
            checks.append({"field":key,"result":"unknown","reason":"Invalid profile or rule value"})
    statuses = {c["result"] for c in checks}
    status = "ineligible" if "fail" in statuses else "insufficient_information" if "unknown" in statuses or not checks else "eligible_by_recorded_rules"
    return {"status":status,"checks":checks,"disclaimer":"Preliminary rule-based screening only; verify current requirements with the official authority."}

def rank_schemes(query, schemes):
    """Actual unsupervised ML baseline: TF-IDF with cosine similarity."""
    if not schemes: return []
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    corpus = [f"{s['name']} {s.get('description','')} {s.get('category','')}" for s in schemes]
    if not (query or '').strip():
        return [{**s,"relevance_score":0.0} for s in schemes]
    try:
        vectors = TfidfVectorizer(ngram_range=(1,2), stop_words='english').fit_transform([query]+corpus)
        scores = cosine_similarity(vectors[0:1], vectors[1:]).ravel()
    except ValueError:
        scores = [0.0]*len(schemes)
    return sorted([{**s,"relevance_score":round(float(score),4)} for s,score in zip(schemes,scores)],key=lambda x:x['relevance_score'],reverse=True)
