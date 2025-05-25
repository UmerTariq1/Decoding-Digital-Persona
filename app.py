import streamlit as st
from src.persona_predictor import load_personas, extract_keywords, score_personas, classify_with_gpt
from src.ui_components import (
    show_loading_animation,
    show_intro_message,
    display_personas_sidebar,
    display_persona_images
)
from src.custom_logger import get_logger

# Initialize logger
logger = get_logger()

# Load personas once
PERSONAS = load_personas('data/personas/personas.yaml')

def process_persona_prediction(bio, posts):
    """Main function to process persona prediction"""
    # Show loading animation
    show_loading_animation()
    
    # Join all posts with spaces
    posts_text = " ".join(posts)
    user_input = bio + " " + posts_text
    
    # Log the query
    logger.info("------------------------------------")
    logger.info(f"Query received - Bio: {bio}, Posts: {posts}")
    
    tokens = extract_keywords(user_input)
    top_personas = score_personas(PERSONAS, tokens, top_n=3)

    # Log rule-based matches
    for persona, score, matched_keywords, confidence in top_personas:
        if score > 0 and matched_keywords:
            logger.info(f"Rule-based match - Persona: {persona['display_name']}, "
                       f"Score: {score}, Keywords: {matched_keywords}, "
                       f"Confidence: {confidence:.1f}%")

    st.subheader(":sparkles: Top Rule-Based Personas :sparkles:")
    shown_any = False
    for idx, (persona, score, matched_keywords, confidence) in enumerate(top_personas, 1):
        if score > 0 and matched_keywords:
            shown_any = True
            icon = persona.get('icon', '')
            st.markdown(f"<div style='display:flex;align-items:center;'><span style='font-size:2rem;margin-right:0.5em;'>{icon}</span> <b style='font-size:1.2rem'>{persona['display_name']}</b>  <span style='background:#4CAF50;color:white;border-radius:8px;padding:0.2em 0.7em;margin-left:0.7em;font-size:1rem;'>Confidence: {confidence:.1f}%</span></div>", unsafe_allow_html=True)
            st.write(f"{persona['description']}")
            st.markdown(f"<b>Key Indicators:</b> {', '.join(matched_keywords)}", unsafe_allow_html=True)
            st.markdown("<hr>", unsafe_allow_html=True)
    if not shown_any:
        st.info("No strong persona matches found for your input.")

    # GPT processing if API key is available
    openai_api_key = st.secrets["general"]["openai_api_key"] if "openai_api_key" in st.secrets["general"] else None
    if openai_api_key:
        gpt_persona, gpt_reasoning = classify_with_gpt(bio, posts_text, [p[0] for p in top_personas if p[1] > 0 and p[2]], openai_api_key)
        
        # Log GPT response
        logger.info(f"GPT Analysis - Selected Persona: {gpt_persona}, Reasoning: {gpt_reasoning}")
        
        if gpt_persona:        
            matching_persona = next((p for p in PERSONAS if p['persona_name'] == gpt_persona), None)
            matching_persona_display_name = matching_persona['display_name']
            
            st.subheader(":crystal_ball: GPT-Analyzed Persona :crystal_ball:")
            st.markdown(f"<div style='font-size:2rem;'>{matching_persona_display_name}</div>", unsafe_allow_html=True)
            st.markdown(f"<b>Reasoning:</b> {gpt_reasoning}", unsafe_allow_html=True)
            
            if matching_persona:
                st.markdown("<hr>", unsafe_allow_html=True)

                display_persona_images(matching_persona)
        else:
            st.info("GPT could not confidently select a persona.")
    else:
        st.info("OpenAI API key not found in secrets.toml.")
    logger.info("------------------------------------")

def main():
    st.set_page_config(page_title="Digital Persona Predictor", page_icon="✨")
    
    # Initialize session state for intro message
    if 'intro_shown' not in st.session_state:
        st.session_state.intro_shown = False
    
    # Show intro message if it hasn't been shown yet
    if not st.session_state.intro_shown:
        show_intro_message()
        st.session_state.intro_shown = True
        st.rerun()
    
    # Display personas in sidebar
    display_personas_sidebar(PERSONAS)
    
    st.title("Digital Persona Predictor ✨")
    st.write("Enter your short bio and a few sample social media posts. We'll predict your digital persona!")

    # Initialize session state for default values
    if 'bio' not in st.session_state:
        st.session_state.bio = ""
    if 'posts' not in st.session_state:
        st.session_state.posts = [""]  
    if 'post_count' not in st.session_state:
        st.session_state.post_count = 1

    # Input fields with unique keys
    bio = st.text_area("Your short bio:", value=st.session_state.bio, key="bio_input")
    
    st.subheader("Your Social Media Posts")
    
    # Display existing post inputs
    for i in range(len(st.session_state.posts)):
        st.text_input(
            f"Post {i+1}:",
            value=st.session_state.posts[i],
            key=f"post_{i}"
        )
    
    # Add Post button
    if st.button("➕ Add Another Post"):
        st.session_state.posts.append("")
        st.session_state.post_count += 1
        st.rerun()

    # Create columns for the buttons
    col1, col2 = st.columns(2)

    with col1:
        predict_button = st.button("Predict Persona")

    with col2:
        fill_defaults = st.button("Fill Test Values", help="Click to fill in sample values for testing")

    # Handle button clicks
    if fill_defaults:
        st.session_state.bio = "Adventurer, Traveler, Tech Enthusiast, Roaming the world"
        st.session_state.posts = [
            "Visited Naples today. Was fun.",
            "Here are the 10 reasons why you should go to Black Forest",
            "I just released a vlog on my stay in Maldives. Go check it out."
        ]
        st.session_state.post_count = 3
        st.rerun()

    if predict_button:
        # Collect all non-empty posts
        valid_posts = [post for post in st.session_state.posts if post.strip()]
        
        if not bio.strip() or not valid_posts:
            st.warning("Please fill in both the bio and at least one post.")
        else:
            process_persona_prediction(bio, valid_posts)

if __name__ == "__main__":
    main() 