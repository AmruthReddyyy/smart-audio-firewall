from topic_loader import load_sensitive_topics

topic_file = "sensitive_topics.json"
topics = load_sensitive_topics(topic_file)

for category, terms in topics.items():
    print(f"{category}:")
    for term in terms:
        print(f"  – {term}")

