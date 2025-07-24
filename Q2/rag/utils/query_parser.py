def detect_sources(query: str):
    query = query.lower()
    sources = []
    if "amazon" in query:
        sources.append("amazon")
    if "bigbasket" in query or "big basket" in query:
        sources.append("bigbasket")
    if not sources:
        sources = ["amazon", "bigbasket"]
    return sources