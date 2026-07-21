"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Default "pop / happy" taste profile.
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.7,
        "likes_acoustic": False,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rank, (song, score, reasons) in enumerate(recommendations, start=1):
        print(f"{rank}. {song['title']} - {song['artist']}  (score: {score:.2f})")
        for reason in reasons:
            print(f"     - {reason}")
        print()


if __name__ == "__main__":
    main()
