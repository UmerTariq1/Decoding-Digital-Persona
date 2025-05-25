import streamlit as st
from src.image_utils import get_image_base64
import time

def show_loading_animation():
    """Show an animated progress bar with fun messages"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Fun loading messages
    messages = [
        "Scanning your digital footprint...",
        "Analyzing your vibe...",
        "Decoding your persona...",
        "Almost there..."
    ]
    
    # Animate progress bar with messages
    for i, message in enumerate(messages):
        progress = (i + 1) / len(messages)
        progress_bar.progress(progress)
        status_text.text(message)
        time.sleep(0.5)  # just for the show off effect
    
    progress_bar.empty()
    status_text.empty()

def show_intro_message(sleep_time=2):
    """Show the intro message for 2 seconds"""
    intro_container = st.empty()
    intro_container.markdown("""
        <div style='display: flex; justify-content: center; align-items: center; height: 100vh;'>
            <div style='text-align: center;'>
                <h1 style='color: #1f77b4; font-size: 2.5em; margin-bottom: 20px;'>
                    Ever wondered what your digital aura says about you?
                </h1>
                <p style='font-size: 1.8em; color: #666;'>
                    Let's decode your vibe! ✨
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    time.sleep(sleep_time)
    intro_container.empty()

def display_personas_sidebar(personas):
    """Display all personas in the sidebar"""
    st.sidebar.title("Available Personas")
    st.sidebar.markdown("---")
    
    for persona in personas:
        st.sidebar.markdown(f"### {persona['icon']} {persona['display_name']}")
        st.sidebar.markdown(f"{persona['description']}")
        st.sidebar.markdown("---")

def display_persona_images(matching_persona):
    """Display the reference images for a persona"""
    st.markdown("### Notable Figures & Influencers")
    
    # CSS for circular images
    st.markdown("""
        <style>
        .circular-image {
            width: 150px;
            height: 150px;
            border-radius: 50%;
            object-fit: contain;
            background-color: #f0f2f6;
            padding: 5px;
            margin: 10px;
        }
        .image-item {
            text-align: center;
            width: 150px;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Notable Figures
    # st.markdown("#### Notable Figures you can get inspired by ")
    col1, col2, col3 = st.columns(3)
    figures = matching_persona.get('notable_figures', [])
    for i, figure in enumerate(figures):
        col = [col1, col2, col3][i]
        with col:
            try:
                image_path = f"data/ref_imgs/{figure}.jpeg"
                st.markdown(f"""
                    <div class="image-item">
                        <img src="data:image/jpeg;base64,{get_image_base64(image_path)}" class="circular-image">
                        <p>{figure}</p>
                    </div>
                """, unsafe_allow_html=True)
            except:
                st.write(f"*{figure}*")
    
    # Notable Influencers
    st.markdown("#### Influencers you might relate to")
    col1, col2, col3 = st.columns(3)
    influencers = matching_persona.get('notable_influencers', [])
    for i, influencer in enumerate(influencers):
        col = [col1, col2, col3][i]
        with col:
            try:
                image_path = f"data/ref_imgs/{influencer}.jpeg"
                st.markdown(f"""
                    <div class="image-item">
                        <img src="data:image/jpeg;base64,{get_image_base64(image_path)}" class="circular-image">
                        <p>{influencer}</p>
                    </div>
                """, unsafe_allow_html=True)
            except:
                st.write(f"*{influencer}*")
    
    # Related Entities
    st.markdown("#### Brands & Organizations related to you")
    col1, col2, col3 = st.columns(3)
    entities = matching_persona.get('related_entities', [])
    for i, entity in enumerate(entities):
        col = [col1, col2, col3][i]
        with col:
            try:
                image_path = f"data/ref_imgs/{entity}.jpeg"
                st.markdown(f"""
                    <div class="image-item">
                        <img src="data:image/jpeg;base64,{get_image_base64(image_path)}" class="circular-image">
                        <p>{entity}</p>
                    </div>
                """, unsafe_allow_html=True)
            except:
                st.write(f"*{entity}*") 