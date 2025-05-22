from sentence_transformers import SentenceTransformer, util

def embed_topics(topic_dict, model):
    """
    Converts topic dictionary into (category, phrase, embedding) tuples.

    Returns:
        List of (category, phrase, embedding_tensor)
    """
    topic_embeddings = []
    for category, phrases in topic_dict.items():
        for phrase in phrases:
            embedding = model.encode(phrase, convert_to_tensor=True)
            topic_embeddings.append((category, phrase, embedding))
    return topic_embeddings


def flag_transcript(transcript_segments, topic_embeddings):
    """
    Flags each transcript segment based on semantic similarity to sensitive topics.

    Args:
        transcript_segments: List of dicts like:
            [{"text": "...", "start": ..., "end": ...}, ...]
        topic_embeddings: List of (category, phrase, embedding_tensor) from embed_topics()

    Returns:
        List of flagged segments with:
        - text, start, end
        - matched_category
        - matched_phrase
        - similarity_score
        - flag_level ("Safe", "Warning", "Critical")
    """
    # ✅ Force CPU to avoid MPS crash on Mac
    model = SentenceTransformer("all-MiniLM-L6-v2", device="cpu")

    results = []
    for segment in transcript_segments:
        text = segment["text"]
        if not text.strip():
            continue

        text_embedding = model.encode(text, convert_to_tensor=True)

        best_score = 0.0
        best_match = None

        for category, phrase, phrase_embedding in topic_embeddings:
            score = util.cos_sim(text_embedding, phrase_embedding).item()
            if score > best_score:
                best_score = score
                best_match = (category, phrase)

        # Flag level by threshold
        if best_score < 0.3:
            flag_level = "Safe"
        elif best_score < 0.6:
            flag_level = "Warning"
        else:
            flag_level = "Critical"

        results.append({
            "text": text,
            "start": segment.get("start"),
            "end": segment.get("end"),
            "matched_category": best_match[0] if best_match else None,
            "matched_phrase": best_match[1] if best_match else None,
            "similarity_score": round(best_score, 3),
            "flag_level": flag_level
        })

    return results

