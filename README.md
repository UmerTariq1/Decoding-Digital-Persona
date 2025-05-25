# Digital Persona Predictor

An intelligent tool that analyzes your digital presence to predict your online persona. By analyzing your bio and social media posts, it identifies patterns and characteristics that define your digital identity.

## Features
- **Smart Analysis**: Uses both rule-based matching and AI-powered classification
- **Multi-Modal Input**: Analyzes both your bio and social media posts
- **Detailed Insights**: Provides confidence scores and key indicators for each persona match
- **AI-Powered Reasoning**: Uses GPT to provide detailed explanations for persona matches
- **Visual Feedback**: Displays relevant persona images and icons

## Technical Features
- Natural Language Processing using spaCy
- Keyword extraction and matching
- GPT-3.5 integration for advanced analysis
- Streamlit-based interactive UI
- Real-time persona scoring and classification

## How to Run
1. Create and activate a virtual environment:
   ```bash
   python3.11 -m venv venv
   source venv/bin/activate
   ```

2. Install requirements:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

3. Start the app:
   ```bash
   streamlit run app.py
   ```

4. To deactivate the virtual environment when done:
   ```bash
   deactivate
   ```

## Project Structure
- `app.py`: Main Streamlit application
- `src/persona_predictor.py`: Core prediction logic
- `src/ui_components.py`: UI components and layouts
- `src/image_utils.py`: Image processing utilities
- `data/personas/`: Persona definitions and assets

## Requirements
- Python 3.11
- OpenAI API key (for GPT analysis)
- spaCy with English language model
- Streamlit
