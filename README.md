# 🎬 Movie Recommendation System

A **Content-Based Movie Recommendation System** built using **Python, Machine Learning, Streamlit, Pandas, Scikit-learn, and the TMDB API**.

The application recommends movies similar to a user's selected movie by analyzing movie metadata such as genres, keywords, cast, crew, and overview. Movie posters are fetched dynamically using the **TMDB API**, providing an interactive and visually appealing user experience.

> **Machine Learning Project | Content-Based Recommendation Engine**

---

# 🌐 Live Demo

**Live App:** `Add Streamlit/Railway/Render URL Here`

---

# 💻 GitHub Repository

**Repository:** `Add GitHub Repository Link Here`

---

# 📖 Table of Contents

- Overview
- Features
- Demo
- Tech Stack
- Project Structure
- Dataset
- Machine Learning Pipeline
- Recommendation Algorithm
- Installation
- Environment Variables
- Running the Project
- API Integration
- Future Improvements
- Known Limitations
- Screenshots
- License

---

# 📌 Overview

The Movie Recommendation System suggests movies similar to the one selected by the user.

Instead of recommending movies based on ratings, this project uses **Content-Based Filtering**, which compares movie features like:

- Genres
- Keywords
- Cast
- Director
- Movie Overview

The similarity between movies is calculated using **Cosine Similarity**, allowing users to receive accurate recommendations based on content rather than popularity.

---

# ✨ Features

- 🎬 Recommend similar movies instantly
- 🖼 Fetch movie posters from TMDB API
- 🔍 Search from thousands of movies
- 🤖 Machine Learning recommendation engine
- ⚡ Fast recommendation generation
- 📱 Responsive Streamlit interface
- 📊 Clean and simple UI
- 🚀 Easy deployment on Streamlit Cloud, Render, or Railway

---

# 🛠 Tech Stack

| Layer | Technology |
|---------|------------|
| Language | Python 3 |
| Frontend | Streamlit |
| Machine Learning | Scikit-learn |
| Data Processing | Pandas |
| Numerical Computing | NumPy |
| API | TMDB API |
| Dataset | TMDB 5000 Movies Dataset |
| Recommendation | Cosine Similarity |
| Model Storage | Pickle |
| Deployment | Streamlit Cloud / Railway / Render |

---

# 📂 Project Structure

```text
movie-recommendation-system/
│
├── app.py
├── movie_list.pkl
├── similarity.pkl
├── requirements.txt
├── README.md
│
├── dataset/
│   ├── tmdb_5000_movies.csv
│   └── tmdb_5000_credits.csv
│
└── notebooks/
    └── Movie Recommendation.ipynb
```

---

# 📊 Dataset

This project uses the **TMDB 5000 Movie Dataset**.

Dataset includes:

- Movie Title
- Genres
- Keywords
- Cast
- Crew
- Overview
- Popularity
- Vote Average
- Release Date

The recommendation model is trained using these movie attributes.

---

# 🤖 Machine Learning Pipeline

The recommendation engine follows these steps:

1. Load movie dataset
2. Merge movies and credits datasets
3. Select important features
4. Handle missing values
5. Extract genres, cast, keywords, and director
6. Create a combined "tags" column
7. Convert text to lowercase
8. Remove spaces
9. Apply stemming
10. Convert text into vectors using CountVectorizer
11. Calculate Cosine Similarity
12. Save processed data using Pickle

---

# 🧠 Recommendation Algorithm

The system uses **Content-Based Filtering**.

Workflow:

```
Movie Selected
        │
        ▼
Extract Features
        │
        ▼
Vectorization
        │
        ▼
Cosine Similarity
        │
        ▼
Top Similar Movies
        │
        ▼
Fetch Posters from TMDB API
        │
        ▼
Display Recommendations
```

---

# 🚀 How Recommendations Work

When a user selects a movie:

- The movie is converted into a feature vector.
- Cosine Similarity compares it with every other movie.
- The top similar movies are selected.
- Poster images are fetched from TMDB.
- Recommended movies are displayed in the UI.

---

# 🖼 TMDB API Integration

Movie posters are fetched dynamically using the **TMDB API**.

Example:

```python
https://api.themoviedb.org/3/movie/{movie_id}?api_key=YOUR_API_KEY
```

The API returns:

- Poster Path
- Movie Title
- Rating
- Release Date
- Overview

---

# ⚙ Installation

## Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/movie-recommendation-system.git

cd movie-recommendation-system
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Run Application

```bash
streamlit run app.py
```

---

Open your browser:

```
http://localhost:8501
```

---

# 🌍 Environment Variables

Create a `.env` file (optional):

```env
TMDB_API_KEY=YOUR_TMDB_API_KEY
```

Or directly add your API key inside `app.py`.

---

# 📦 Requirements

```
streamlit
pandas
numpy
scikit-learn
requests
nltk
```

Install all dependencies using:

```bash
pip install -r requirements.txt
```

---

# 📈 Future Improvements

- Collaborative Filtering
- Hybrid Recommendation System
- Deep Learning Recommendations
- User Login
- Watchlist Feature
- Movie Ratings
- Personalized Recommendations
- Genre Filtering
- Trailer Integration
- IMDb Rating Integration
- Recommendation History

---

# ⚠ Known Limitations

- Recommendations are content-based only.
- No user personalization.
- Requires TMDB API for posters.
- Dataset is limited to TMDB 5000 movies.
- Similarity matrix can become large for very large datasets.

---

# 📷 Screenshots

Add screenshots of:

- Home Page
- Recommendation Results
- Movie Posters
- Streamlit Interface

Example:

```
screenshots/
│
├── home.png
├── recommendation.png
└── results.png
```

---

# 🧪 Example

**Input**

```
Avatar
```

**Output**

```
Titan A.E.
John Carter
Guardians of the Galaxy
The Fifth Element
Star Trek
```

*(Recommendations may vary depending on the trained model.)*

---

# 🔒 Project Highlights

- ✅ Machine Learning Project
- ✅ Content-Based Filtering
- ✅ Cosine Similarity
- ✅ TMDB API Integration
- ✅ Streamlit Web Application
- ✅ Responsive UI
- ✅ Pickle Model Serialization
- ✅ Easy Deployment

---

# 🚀 Deployment

The application can be deployed on:

- Streamlit Community Cloud
- Railway
- Render
- Hugging Face Spaces

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch

```bash
git checkout -b feature-name
```

3. Commit changes

```bash
git commit -m "Added new feature"
```

4. Push to GitHub

```bash
git push origin feature-name
```

5. Open a Pull Request

---

# 📄 License

This project is developed for learning purposes and showcases the implementation of a **Content-Based Movie Recommendation System using Machine Learning**.

---

# 👨‍💻 Developer

**Devesh Prajapati**

- 💼 Aspiring Machine Learning Engineer
- 🐍 Python Developer
- 📊 Data Analytics Enthusiast
- 🤖 Machine Learning Developer

---

## ⭐ If you found this project helpful, consider giving it a star on GitHub!
