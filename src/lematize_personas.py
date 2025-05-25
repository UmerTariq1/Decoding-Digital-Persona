# this script was only used once to lemmatize the personas.yaml file
import yaml
import spacy

# Load spaCy English model
nlp = spacy.load("en_core_web_trf")

# Load the YAML file
with open("personas.yaml", "r") as f:
    data = yaml.safe_load(f)

# Function to lemmatize list of words
def lemmatize_list(words):
    lemmatized = []
    for word in words:
        doc = nlp(word)
        lemmas = [token.lemma_ for token in doc]
        lemmatized.append(" ".join(lemmas))
    return list(set(lemmatized)) # set list to remove duplicates

for persona in data:
    print(f"persona : {persona['persona_name']}")
    
    if "keywords" in persona:
        print(f"keywords : {persona['keywords']}")
        persona["keywords"] = lemmatize_list(persona["keywords"])
        print(f"keywords : {persona['keywords']}")

    if "negative_keywords" in persona:
        print(f"negative_keywords : {persona['negative_keywords']}")
        persona["negative_keywords"] = lemmatize_list(persona["negative_keywords"])
        print(f"negative_keywords : {persona['negative_keywords']}")

    print("-"*100)

# Save the updated YAML
with open("personas_lemmatized.yaml", "w") as f:
    yaml.dump(data, f, allow_unicode=True)

print("Lemmatization complete. Output saved to personas_lemmatized.yaml")
