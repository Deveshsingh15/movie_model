import streamlit as st
import pickle
import requests
import os
import numpy as np
from concurrent.futures import ThreadPoolExecutor

# -------------------- PAGE CONFIG --------------------

st.set_page_config(
    page_title="Movie Recommender",
    page_icon="🎬",
    layout="wide"
)

# -------------------- LOAD MODEL --------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "movie_model.pkl")

try:
    with open(model_path, "rb") as f:
        data = pickle.load(f)

    movies = data["movies"]
    similarity = data["similarity"]

except:
    st.error("❌ movie_model.pkl not found or corrupted")
    st.stop()

# -------------------- OMDB + TMDB API KEYS --------------------
# OMDB is our primary poster source.  
# You can get a free OMDB key from https://www.omdbapi.com/apikey.aspx.
# We also support TMDB as a fallback if OMDB doesn't have a poster.
# Treat blank environment variables as unset so defaults still apply.
OMDB_API_KEY = os.getenv("OMDB_API_KEY") or "23ed64f4"  # default from user
TMDB_API_KEY = os.getenv("TMDB_API_KEY") or ""
# (API key warnings shown below; remove debug printing)

# -------------------- FETCH POSTER FUNCTION --------------------
# memoize OMDB/TMDB lookups to avoid hitting API limits and speed up UI.
# include the current API keys in the cache key so that changing or adding
# a key automatically invalidates any stale placeholder results.
@st.cache_data(show_spinner=False)
def fetch_poster(title: str, omdb_key: str = OMDB_API_KEY, tmdb_key: str = TMDB_API_KEY) -> str:
    """Return a poster URL for the given movie title.

    First try OMDB, then fall back to TMDB search if OMDB fails or isn't
    configured.  If both APIs are unavailable, returns a placeholder.
    """
    # helper for TMDB lookup
    def _tmdb_lookup(name):
        try:
            query = requests.utils.quote(name)
            url = (
                f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}"
                f"&query={query}"
            )
            r = requests.get(url, timeout=10)
            r.raise_for_status()
            results = r.json().get("results") or []
            if results:
                path = results[0].get("poster_path")
                if path:
                    return f"https://image.tmdb.org/t/p/w500{path}"
        except Exception:
            pass
        return None

    # try OMDB first
    if omdb_key:
        try:
            query = requests.utils.quote(title)
            url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t={query}"
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            poster = data.get("Poster")
            if poster and poster != "N/A":
                return poster
        except Exception:
            pass

    # OMDB failed or not configured; try TMDB if we have a key
    if tmdb_key:
        tmdb_poster = _tmdb_lookup(title)
        if tmdb_poster:
            return tmdb_poster

    # ultimate fallback
    if not omdb_key and not tmdb_key:
        return "https://via.placeholder.com/500x750?text=No+API+Keys"
    return "https://via.placeholder.com/500x750?text=No+Poster"

# -------------------- RECOMMENDATION LOGIC --------------------

@st.cache_data(show_spinner=False)
def recommend(movie):
    """Return five similar titles.

    Caching avoids redoing the search on each rerun.
    """
    if movie not in movies["title"].values:
        return []
    index = movies[movies["title"] == movie].index[0]
    sim_row = similarity[index]
    top_idx = np.argpartition(sim_row, -6)[-6:]
    top_idx = top_idx[np.argsort(sim_row[top_idx])[::-1]]
    names = []
    for idx in top_idx[1:6]:
        names.append(movies.iloc[idx].title)
    return names

# -------------------- UI --------------------

# custom styles for a nicer poster grid and hide default menu/footer
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .row {display: flex; justify-content: space-around; flex-wrap: wrap;}
    .card {box-shadow: 0 4px 8px rgba(0,0,0,0.2); transition: 0.3s; width: 18%; margin: 5px;}
    .card:hover {box-shadow: 0 8px 16px rgba(0,0,0,0.2);}
    .card img {width:100%;}
    .container {padding:2px 16px; text-align:center;}
    .container h4 {margin:5px 0; font-size:1rem;}
    @media (max-width:768px) {.card {width:45%;}}
    @media (max-width:480px) {.card {width:90%;}}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🎬 Movie Recommender System")
st.write("Select a movie and get similar movie recommendations with official posters.")

movie_list = movies["title"].values
selected_movie = st.selectbox(
    "Type or select a movie",
    movie_list
)

# clear any cached posters produced before API key was set
st.cache_data.clear()

if st.button("Show Recommendation 🚀"):
    with st.spinner("Finding recommendations…"):
        names = recommend(selected_movie)

    if names:
        # fetch poster URLs for the titles in parallel
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(fetch_poster, name) for name in names]
            posters_list = [f.result() for f in futures]

        # render in standard Streamlit columns
        cols = st.columns(len(names))
        for col, name, poster in zip(cols, names, posters_list):
            with col:
                st.image(poster, use_container_width=True)
                st.caption(name)
    else:
        st.warning("No recommendations found ⚠️")