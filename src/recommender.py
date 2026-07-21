import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

# Sample user taste profile for Phase 2 (used for manual testing and examples).
SAMPLE_USER_PROFILE = UserProfile(
    favorite_genre="synthwave",
    favorite_mood="energetic",
    target_energy=0.75,
    likes_acoustic=False,
)

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into a list of dicts with typed numeric fields."""
    float_fields = ("energy", "tempo_bpm", "valence", "danceability", "acousticness")
    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            row["id"] = int(row["id"])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against user_prefs; return (total_score, reasons)."""
    score = 0.0
    reasons: List[str] = []

    if song["genre"] == user_prefs["favorite_genre"]:
        score += 2.0
        reasons.append("genre match (+2.0)")

    if song["mood"] == user_prefs["favorite_mood"]:
        score += 1.0
        reasons.append("mood match (+1.0)")

    energy_points = 1.0 * (1 - abs(song["energy"] - user_prefs["target_energy"]))
    if energy_points != 0:
        score += energy_points
        reasons.append(f"energy close to target (+{energy_points:.2f})")

    if user_prefs["likes_acoustic"]:
        acoustic_points = 0.5 * song["acousticness"]
    else:
        acoustic_points = 0.5 * (1 - song["acousticness"])
    if acoustic_points != 0:
        score += acoustic_points
        reasons.append(f"matches acoustic preference (+{acoustic_points:.2f})")

    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, List[str]]]:
    """Score all songs and return the top-k as (song, score, reasons), highest first."""
    scored = [(song, *score_song(user_prefs, song)) for song in songs]
    # Use sorted() (not songs.sort()) so we return a new ranked list without
    # mutating the caller's `songs` list -- reordering their input in place
    # would be a surprising side effect.
    ranked = sorted(scored, key=lambda result: result[1], reverse=True)
    return ranked[:k]
