"""Create the compact recommendation artifact used by the deployed app.

Run this script locally whenever ``movies.pkl`` or ``similarity.pkl`` changes.
The source pickle files are intentionally ignored because the similarity matrix
is too large for a normal Git repository.
"""

import argparse
import pickle
from pathlib import Path

import numpy as np


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--movies", type=Path, default=Path("movies.pkl"))
    parser.add_argument("--similarity", type=Path, default=Path("similarity.pkl"))
    parser.add_argument(
        "--output", type=Path, default=Path("recommendation_model.npz")
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    with args.movies.open("rb") as movies_file:
        movies = pickle.load(movies_file)
    with args.similarity.open("rb") as similarity_file:
        similarity = pickle.load(similarity_file)

    if "title" not in movies.columns:
        raise ValueError("movies.pkl does not contain a 'title' column")

    movie_count = len(movies)
    if similarity.shape != (movie_count, movie_count):
        raise ValueError(
            f"similarity.pkl has shape {similarity.shape}; "
            f"expected {(movie_count, movie_count)}"
        )
    if movie_count > np.iinfo(np.uint16).max:
        raise ValueError("Use a wider index dtype for more than 65,535 movies")

    titles = np.asarray(movies["title"].astype(str).tolist(), dtype=np.str_)
    recommendation_indices = np.empty((movie_count, 5), dtype=np.uint16)

    for movie_position, scores in enumerate(similarity):
        ranked_positions = np.argsort(scores)[::-1]
        top_five = ranked_positions[ranked_positions != movie_position][:5]
        if len(top_five) != 5:
            raise ValueError(f"Could not find five recommendations for row {movie_position}")
        recommendation_indices[movie_position] = top_five

    np.savez_compressed(
        args.output,
        titles=titles,
        recommendation_indices=recommendation_indices,
    )
    print(
        f"Created {args.output} with {movie_count:,} movies "
        f"({args.output.stat().st_size / 1024:.1f} KiB)"
    )


if __name__ == "__main__":
    main()
