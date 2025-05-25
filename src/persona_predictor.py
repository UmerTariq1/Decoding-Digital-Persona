import yaml
import re
from collections import Counter
from typing import List, Dict, Tuple
import openai
import spacy
from src.custom_logger import get_logger

# Initialize logger
logger = get_logger()
nlp = spacy.load("en_core_web_sm")
STOPWORDS = set(['the', 'and', 'is', 'in', 'to', 'of', 'a', 'for', 'on', 'with', 'at', 'by', 'an', 'be', 'this', 'that', 'it'])

# Load personas from YAML
def load_personas(yaml_path: str) -> List[Dict]:
    with open(yaml_path, 'r') as f:
        return yaml.safe_load(f)

# Extract keywords/entities using spaCy
def extract_keywords(text: str) -> List[str]:
    doc = nlp(text)
    keywords = set([ent.text.lower() for ent in doc.ents])
    keywords.update(chunk.text.lower() for chunk in doc.noun_chunks)
    keywords.update([token.lemma_.lower() for token in doc if not token.is_stop and not token.is_punct])

    keywords = list(keywords)

    keywords_update = []
    for i in range(len(keywords)):
        # add each token in the keyword to the keywords_update
        for token in keywords[i].split():
            keywords_update.append(token)

    keywords_update = list(set(keywords_update))
    keywords_lemmatized = []
    for keyword in keywords_update:
        doc = nlp(keyword)
        keywords_lemmatized.append(doc[0].lemma_)
    

    return list(keywords_lemmatized)
 


def preprocess_text(text: str) -> List[str]:
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    tokens = text.split()
    return [t for t in tokens if t not in STOPWORDS]

# Score personas by keyword match, return top n personas
def score_personas(personas: List[Dict], tokens: List[str], top_n: int = 3) -> List[Tuple[Dict, int, List[str], float]]:
    scores = []
    token_counts = Counter(tokens)
    
    for persona in personas:
        score = 0
        matched_keywords = []
        # print(f"persona : {persona['display_name']}")
        for kw in persona.get('keywords', []):
            if kw.lower() in token_counts:
                score += token_counts[kw.lower()]
                matched_keywords.append(kw)
                # print(f"Matched kw : {kw}")
        for nkw in persona.get('negative_keywords', []):
            if nkw.lower() in token_counts:
                # score -= token_counts[nkw.lower()]
                score -= 0.3
                # print(f"Matched nkw : {nkw}")

        scores.append((persona, score, matched_keywords))
    
    # Calculate total of positive scores for normalization
    total_positive_score = sum(max(0, score) for _, score, _ in scores)
    
    # Add confidence percentage to each score tuple
    scores_with_confidence = []
    for persona, score, matched_keywords in scores:
        # Ensure score is non-negative
        normalized_score = max(0, score)
        # Calculate confidence as percentage of total positive scores
        confidence = (normalized_score / total_positive_score * 100) if total_positive_score > 0 else 0
        scores_with_confidence.append((persona, score, matched_keywords, confidence))
    
    # Sort by score in descending order
    scores_with_confidence.sort(key=lambda x: x[1], reverse=True)

    # if all scores are 0, return all the personas
    if all(score == 0 for _, score, _, _ in scores_with_confidence):
        return scores_with_confidence
    else:
        return scores_with_confidence[:top_n]

# Stub for LLM explanation (not used if classify_with_gpt is used)
def generate_explanation(persona: Dict, matched_keywords: List[str], user_input: str) -> str:
    return f"You seem like a {persona['display_name']} because you mentioned: {', '.join(matched_keywords)}."

def load_gpt_prompt_template(path: str = "data/gpt_prompt.txt") -> str:
    '''
    Reads the GPT prompt template from the prompt file and returns it as a string.
    '''
    with open(path, "r") as f:
        return f.read()

# Call OpenAI GPT model for persona classification and reasoning, using only top personas
def classify_with_gpt(bio: str, posts: str, top_personas: List[Dict], openai_api_key: str) -> Tuple[str, str]:
    '''
    This function uses the OpenAI GPT model to classify the user's input into a persona.
    Args : 
        bio : str
        posts : str
        top_personas : List[Dict]
        openai_api_key : str
    Returns :
        persona : str
        reasoning : str
    '''
    prompt_template = load_gpt_prompt_template()
    persona_list = ', '.join([p['persona_name'] for p in top_personas])
    persona_descriptions = '\n'.join([f"{p['persona_name']}: {p['description']}" for p in top_personas])
    prompt = prompt_template.format(
        persona_list=persona_list,
        persona_descriptions=persona_descriptions,
        bio=bio,
        posts=posts
    )
    
    # Log the GPT prompt
    logger.info("********************")
    logger.info(f"GPT Prompt : {prompt}")
    logger.info("********************")
    
    client = openai.OpenAI(api_key=openai_api_key)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=256,
        temperature=0.3
    )
    content = response.choices[0].message.content
    
    # Log the raw GPT response
    logger.info("+++++++++++++++++++++++++++++++++++++")
    logger.info(f"Raw GPT Response:\n{content}")
    logger.info("+++++++++++++++++++++++++++++++++++++")
    
    persona = ""
    reasoning = ""
    for line in content.splitlines():
        if line.lower().startswith("persona:"):
            persona = line.split(":", 1)[1].strip()
        elif line.lower().startswith("reasoning:"):
            reasoning = line.split(":", 1)[1].strip()
    return persona, reasoning 