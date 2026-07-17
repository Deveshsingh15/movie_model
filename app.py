import os
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
import requests
import streamlit as st


st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide",
)

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "recommendation_model.npz"


@st.cache_resource(show_spinner="Loading recommendation model...")
def load_model():
    """Load and validate the compact model artifact shipped with the app."""
    with np.load(MODEL_PATH, allow_pickle=False) as model_data:
        titles = model_data["titles"]
        recommendation_indices = model_data["recommendation_indices"]

    if titles.ndim != 1 or not len(titles):
        raise ValueError("The model must contain a non-empty one-dimensional title list")
    if recommendation_indices.shape != (len(titles), 5):
        raise ValueError(
            "The model must contain exactly five recommendations for every title"
        )
    if np.any(recommendation_indices >= len(titles)):
        raise ValueError("The model contains an out-of-range recommendation index")

    return titles, recommendation_indices


try:
    movie_titles, recommendation_indices = load_model()
except (
    OSError,
    EOFError,
    KeyError,
    ValueError,
) as exc:
    st.error(
        "Could not load the recommendation model. Make sure "
        "`recommendation_model.npz` is in the same folder as `app.py`."
    )
    st.code(str(exc))
    st.stop()


# OMDb is the primary poster source; TMDB is an optional fallback.
OMDB_API_KEY = os.getenv("OMDB_API_KEY") or ""
TMDB_API_KEY = os.getenv("TMDB_API_KEY") or ""
POSTER_PLACEHOLDER = "https://placehold.co/500x750?text=No+Poster"


@st.cache_data(show_spinner=False, ttl=24 * 60 * 60)
def fetch_poster(
    title: str,
    omdb_key: str = OMDB_API_KEY,
    tmdb_key: str = TMDB_API_KEY,
) -> str:
    """Return an OMDb or TMDB poster URL, falling back to a placeholder."""
    if omdb_key:
        try:
            response = requests.get(
                "https://www.omdbapi.com/",
                params={"apikey": omdb_key, "t": title},
                timeout=10,
            )
            response.raise_for_status()
            poster = response.json().get("Poster")
            if poster and poster != "N/A":
                return poster
        except (requests.RequestException, ValueError):
            pass

    if tmdb_key:
        try:
            response = requests.get(
                "https://api.themoviedb.org/3/search/movie",
                params={"api_key": tmdb_key, "query": title},
                timeout=10,
            )
            response.raise_for_status()
            results = response.json().get("results") or []
            if results and results[0].get("poster_path"):
                return f"https://image.tmdb.org/t/p/w500{results[0]['poster_path']}"
        except (requests.RequestException, ValueError):
            pass

    return POSTER_PLACEHOLDER


@st.cache_data(show_spinner=False)
def recommend(movie: str) -> list[str]:
    """Return the five most similar movie titles."""
    matches = np.flatnonzero(movie_titles == movie)
    if not len(matches):
        return []

    movie_position = int(matches[0])
    return [
        str(movie_titles[position])
        for position in recommendation_indices[movie_position]
    ]


st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🎬 Movie Recommender System")
st.write("Select a movie and get five similar recommendations with posters.")

movie_list = movie_titles.tolist()
selected_movie = st.selectbox("Type or select a movie", movie_list)

if st.button("Show recommendations 🚀", type="primary"):
    with st.spinner("Finding recommendations..."):
        names = recommend(selected_movie)

    if names:
        with ThreadPoolExecutor(max_workers=len(names)) as executor:
            posters = list(executor.map(fetch_poster, names))

        for column, name, poster in zip(st.columns(len(names)), names, posters):
            with column:
                st.image(poster, width="stretch")
                st.caption(name)
    else:
        st.warning("No recommendations found.")
