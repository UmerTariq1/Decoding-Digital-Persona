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
1. Install requirements:
   ```
   pip install -r requirements.txt
   ```
2. Start the app:
   ```
   streamlit run app.py
   ```

## Project Structure
- `app.py`: Main Streamlit application
- `src/persona_predictor.py`: Core prediction logic
- `src/ui_components.py`: UI components and layouts
- `src/image_utils.py`: Image processing utilities
- `data/personas/`: Persona definitions and assets

## Requirements
- Python 3.7+
- OpenAI API key (for GPT analysis)
- spaCy with English language model
- Streamlit

## Next Steps
- Integrate LLM for smarter explanations
- Add more personas and features 