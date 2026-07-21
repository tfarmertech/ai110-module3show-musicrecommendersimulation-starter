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

    # Named taste profiles evaluated in Phase 4.
    profiles = {
        # Default "pop / happy" taste profile.
        "Default Pop/Happy": {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.7,
            "likes_acoustic": False,
        },
        "High-Energy Pop": {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.9,
            "likes_acoustic": False,
        },
        "Chill Lofi": {
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 0.2,
            "likes_acoustic": True,
        },
        "Deep Intense Rock": {
            "favorite_genre": "rock",
            "favorite_mood": "intense",
            "target_energy": 0.85,
            "likes_acoustic": False,
        },
        # Adversarial edge cases (see step 2 write-up):
        # Conflicting signals: a low-energy mood paired with a very high energy target.
        "Adversarial: Calm Mood, High Energy": {
            "favorite_genre": "classical",
            "favorite_mood": "melancholic",
            "target_energy": 0.95,
            "likes_acoustic": True,
        },
        # Impossible taste: genre AND mood that appear nowhere in songs.csv.
        "Adversarial: Absent Genre & Mood": {
            "favorite_genre": "disco",
            "favorite_mood": "romantic",
            "target_energy": 0.6,
            "likes_acoustic": False,
        },
    }

    for name, user_prefs in profiles.items():
        print("\n" + "=" * 64)
        print(name)
        print("=" * 64)
        recommendations = recommend_songs(user_prefs, songs, k=5)
        for rank, (song, score, reasons) in enumerate(recommendations, start=1):
            print(f"{rank}. {song['title']} - {song['artist']}  (score: {score:.2f})")
            for reason in reasons:
                print(f"     - {reason}")
            print()


if __name__ == "__main__":
    main()
