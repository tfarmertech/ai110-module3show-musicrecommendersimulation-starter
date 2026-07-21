# 🎵 Music Recommender Simulation

## Project Summary

VibeFinder 1.0 is a content-based music recommender that suggests songs from an 18-track catalog based on a listener's genre, mood, energy, and acousticness preferences. It scores every song in the catalog against a user's taste profile using a weighted point system (genre and mood matches, plus closeness on two numeric features), then ranks the results and explains each recommendation with a plain-language list of what matched. There's no collaborative filtering and no other users — every recommendation is a direct, transparent comparison between one song and one listener's stated preferences.
---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

Real platforms blend collaborative filtering (predicting your taste from what similar users liked) with content-based filtering (matching a song's own attributes — genre, mood, energy — to your stated preferences). Spotify and TikTok lean on collaborative filtering at scale for its cultural pattern-matching, but use content-based signals for new songs and explainability. My version is purely content-based: no other users, just a direct comparison between a song's attributes and one UserProfile. Each Song uses genre and mood (exact-match categorical features) plus energy and acousticness (numeric 0–1 features scored by closeness to a target). Each UserProfile mirrors this with favorite_genre, favorite_mood, target_energy, and likes_acoustic. Genre matches are weighted highest, mood next, then the two numeric closeness scores — the Recommender sums these into a score per song and ranks the catalog to produce the top-N list. I left out tempo_bpm and danceability (they track energy too closely) and valence (overlaps with mood) as candidates for later experiments.

**Overview.** This is a purely *content-based* recommender: there are no other users and no collaborative filtering. It compares each song's own attributes against a single `UserProfile` and ranks the catalog by how well they match.

**The catalog.** `data/songs.csv` holds 18 songs. Each has categorical tags (`genre`, `mood`) and numeric audio features on a 0.0–1.0 scale (`energy`, `valence`, `danceability`, `acousticness`) plus `tempo_bpm`.

**Song features used.** `genre` and `mood` (categorical, scored by exact match) and `energy` and `acousticness` (numeric, scored by closeness). `tempo_bpm` and `danceability` are left out (they track `energy`) and `valence` is left out (overlaps `mood`) — kept as later experiments.

**UserProfile.** Stores `favorite_genre`, `favorite_mood`, `target_energy`, and `likes_acoustic`. The sample profile is `synthwave` / `energetic` / `target_energy=0.75` / `likes_acoustic=False`.

### Algorithm Recipe

The `Recommender` scores every song against the `UserProfile` as the sum of:

| Signal | Points | How it's measured |
|---|---|---|
| Genre match | +2.0 | `song.genre == favorite_genre` |
| Mood match | +1.0 | `song.mood == favorite_mood` |
| Energy closeness | up to +1.0 | `1 − abs(song.energy − target_energy)` |
| Acousticness fit | +0.5 | `song.acousticness` agrees with `likes_acoustic` |

Songs are sorted by total score (highest first) and the top *K* are returned, each with a short reason listing which signals matched.

**Worked example.** For the sample profile, *"Night Drive Loop"* (synthwave, moody, energy 0.75, acousticness 0.22) scores +2.0 (genre) + 0 (mood) + 1.0 (energy on target) + 0.5 (low acousticness matches `likes_acoustic=False`) = **3.5**, near the top.

### Potential biases

- **Genre over-prioritization:** Genre's +2.0 weight lets a genre-only match outrank a better mood/energy fit tagged differently — a "filter bubble."
- **Exact-match blind spots:** Close tags like "pop" vs "indie pop" score zero on genre.
- **Tiny catalog:** With 18 songs, one genre/mood can dominate, and unseen tastes can't surface.

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
Loaded songs: 18
Top recommendations:
1. Sunrise City - Neon Echo  (score: 4.29)
     - genre match (+2.0)
     - mood match (+1.0)
     - energy close to target (+0.88)
     - matches acoustic preference (+0.41)
2. Gym Hero - Max Pulse  (score: 3.25)
     - genre match (+2.0)
     - energy close to target (+0.77)
     - matches acoustic preference (+0.47)
3. Rooftop Lights - Indigo Parade  (score: 2.27)
     - mood match (+1.0)
     - energy close to target (+0.94)
     - matches acoustic preference (+0.33)
4. Sundial Groove - The Brasswork  (score: 1.34)
     - energy close to target (+0.92)
     - matches acoustic preference (+0.42)
5. Night Drive Loop - Neon Echo  (score: 1.34)
     - energy close to target (+0.95)
     - matches acoustic preference (+0.39)

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

I ran a weight-sensitivity experiment: doubling the energy weight (1.0 → 2.0) while halving the genre weight (2.0 → 1.0), then comparing the top-5 results for several profiles before reverting the change. For the Default Pop/Happy profile, this flipped the #1 result from Gym Hero to Rooftop Lights — proof that under the original weights, a genre match alone was strong enough to beat a song with a much closer energy fit. I also stress-tested the system across six user profiles (four realistic, two adversarial with conflicting or nonexistent preference combinations) to see how consistently it behaved. The main pattern I found: Gym Hero and Sunrise City dominated 4 of 6 profiles' top 5, not because they were universally great fits, but because the catalog has so few songs per genre that the genre bonus overwhelms everything else once it applies.

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

The catalog is tiny — 18 songs across 15 genres means most genres have exactly one representative track, so the recommender often isn't really ranking anything within a genre, it's just returning the one song that exists. It has no understanding of lyrics, instrumentation, or subjective "vibe" beyond the four numbers and two tags each song carries — two songs that feel completely different to a human listener can score identically if their genre, mood, energy, and acousticness happen to line up. It also clearly over-favors genre: the +2.0 genre-match weight can let a same-genre song beat a much better mood/energy fit tagged differently, which is the same filter-bubble dynamic real-world content-based recommenders create at scale. See model_card.md for a deeper breakdown with specific evidence from testing.

## Reflection

Working through this project made the abstract idea of "recommenders turn data into predictions" feel concrete rather than theoretical. Watching a single weight change flip which song ranked #1 was the clearest moment of that — it's easy to say a scoring system reflects its weights, but seeing Gym Hero lose the top spot the instant I rebalanced energy against genre made it obvious how much of what looks like "taste-matching" is really just arithmetic that happens to line up with intuition often enough to feel meaningful.

The bias risks were the more sobering part. Even with only four features and simple weighted addition — nothing close to a real recommendation engine — the system still produced a narrowing effect: a handful of songs kept resurfacing across unrelated user profiles, and one underlying cause (severe genre imbalance in the catalog) was something I only found by deliberately testing adversarial profiles and comparing results across them rather than just trusting the first output that looked reasonable. That's probably the biggest lesson from this project: a recommender doesn't need to be sophisticated to create a filter bubble — it just needs one dominant, poorly-balanced signal and a dataset too small to give that signal real competition.



