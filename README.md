# Mood Flow

Mood Flow is an AI-powered mood recommendation app built with Python and Streamlit. It detects a user's mood from natural language text and recommends simple, helpful actions based on the detected emotion.

## Live Demo

Try the app here: [https://mooodflow.streamlit.app/](https://mooodflow.streamlit.app/)

## Features

- Detects mood from plain text input
- Shows model confidence scores for predicted moods
- Generates personalized action recommendations
- Supports feedback with helpful and not-for-me ratings
- Tracks user mood history and liked actions
- Uses a clean, professional light-themed Streamlit interface

## Tech Stack

- Python
- Streamlit
- scikit-learn
- TF-IDF Vectorization
- Logistic Regression
- JSON-based local user memory

## How It Works

1. The user enters how they are feeling.
2. The app converts the text into TF-IDF features.
3. A Logistic Regression model predicts the most likely mood.
4. The recommendation engine returns actions linked to that mood.
5. User feedback helps rank future recommendations.

## Project Structure

```text
mood-flow/
├── app.py             # Main Streamlit app and UI
├── engine.py          # Mood classifier, user memory, recommendation engine
├── data.py            # Mood metadata
├── model.py           # Mood-to-activity recommendation data
├── data_handler.py    # JSON data read/write helpers
├── utils.py           # Helper functions
├── requirements.txt   # Python dependencies
└── README.md          # Project documentation
```

## Run Locally

Clone the repository:

```bash
git clone https://github.com/ashishkumar2005/mood-flow.git
cd mood-flow
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start the Streamlit app:

```bash
streamlit run app.py
```

## Deployment

This app is deployed on Streamlit Community Cloud from the `main` branch.

```text
Repository: ashishkumar2005/mood-flow
Branch: main
Main file: app.py
```

## Future Improvements

- Add a larger training dataset
- Improve recommendation ranking with richer feedback signals
- Add charts for mood trends over time
- Add authentication for persistent user profiles
- Store user history in a cloud database

## Author

Built by [Ashish Kumar](https://github.com/ashishkumar2005).
