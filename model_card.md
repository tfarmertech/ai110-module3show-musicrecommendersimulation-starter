# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  
VibeFinder 1.0
---

## 2. Intended Use  

VibeFinder suggests the top 5 songs from an 18-song catalog based on a listener's stated genre, mood, energy, and acousticness preferences. It assumes the user can articulate their taste directly (a favorite genre and mood, a target energy level, and whether they like acoustic sound) rather than inferring taste from listening history. This is a classroom exploration project — a simplified model built to understand how content-based recommenders work, not a production system for real listeners. It works best as a teaching tool for showing how scoring weights shape rankings, not as a music discovery app.

## 3. How the Model Works  

VibeFinder looks at four things about each song: its genre, its mood, how energetic it is, and how acoustic it sounds. It compares these to what a listener says they want. If the song's genre matches the listener's favorite genre, it earns 2 points — the biggest single bonus. If the mood matches, it earns 1 point. Then it checks how close the song's energy is to the listener's target energy, awarding up to 1 point for a near-perfect match. Finally, it checks whether the song's acoustic level agrees with whether the listener likes acoustic sound, awarding up to half a point. All four scores get added together, and the songs with the highest total scores are recommended, along with a plain-language list of which of these things matched. The main change from the starter logic: the scoring function now returns why a song scored the way it did, not just the number.

## 4. Data  
The catalog has 18 songs, up from the original 10 in the starter file. Each song has a genre, a mood, and four numeric features (energy, tempo, valence, danceability, acousticness), all on consistent scales. 15 different genres and a wide range of moods are represented, from happy and chill to angry and melancholic. The dataset is still very small — most genres have exactly one song, so it's more of a proof-of-concept catalog than a realistic music library. Genuine musical nuance (subgenres, lyrical themes, instrumentation) isn't captured at all; a song is only as rich as its four numbers and two tags.
## 5. Strengths  

The system works well for users whose taste maps cleanly onto one existing genre and mood combination in the catalog — for those cases, it reliably surfaces the one song that fits and explains exactly why. It also handles energy preferences gracefully: even without a genre or mood match, the energy-closeness formula correctly favors songs that are numerically similar to the target, which matched my intuition in testing (a "chill lofi" profile pulled toward genuinely low-energy tracks, not random ones). The reason-list output is a real strength — it makes an otherwise opaque score explainable in one glance, which is exactly what the rubric asks for.

## 6. Limitations and Bias 


Features it does not consider: The system ignores tempo_bpm, danceability, and valence entirely — it only scores on genre, mood, energy, and acousticness. This means two songs with wildly different tempos or "positivity" can score identically if their genre/mood/energy/acousticness line up, even if one would feel completely different to a listener.

Genres or moods that are underrepresented: 13 of the 15 genres in the catalog have exactly one song. This turns the +2.0 genre-match weight into a near-deterministic lookup rather than a real ranking signal — a rock fan always gets Storm Runner because there's no other rock song to compare it against, regardless of mood or energy fit.

Cases where the system overfits to one preference: For the High-Energy Pop profile, Sunrise City won with a 4.33 score almost entirely because it's the only pop+happy song in the dataset — the +3.0 categorical bonus (genre + mood) dominated before energy or acousticness had any real chance to differentiate. The ranking is technically correct, but it's really "the only option," not "the best of several."

Ways the scoring might unintentionally favor some users: A cluster of five low-acousticness songs (≤0.10) acts as a universal fallback for any profile with likes_acoustic=False. Gym Hero and Sunrise City each showed up in 4 of the 6 test profiles' top 5 — including profiles with no genre or mood overlap — meaning users with very different stated tastes still converge on the same handful of songs. A weight-sensitivity test confirmed this: doubling the energy weight and halving the genre weight flipped the #1 result for Default Pop/Happy (Rooftop Lights overtook Gym Hero), showing that genre alone — not a holistic fit — was deciding the winner under the original weights.

---

## 7. Evaluation  

Which user profiles you tested: Four realistic profiles (Default Pop/Happy, High-Energy Pop, Chill Lofi, Deep Intense Rock) and two adversarial profiles designed to probe conflicting preferences (e.g. a sad mood paired with high target energy) and a genre/mood combination that doesn't exist anywhere in the catalog.

What you looked for in the recommendations: Whether the top-ranked song for each profile actually matched the "vibe" I'd expect a human to pick, and whether different profiles produced meaningfully different top-5 lists rather than converging on the same songs.

What surprised you: How often the same two or three songs appeared at the top regardless of profile. Gym Hero and Sunrise City dominated 4 of 6 test runs, which wasn't because they were universally excellent fits — it was because the genre-match bonus is large enough to overwhelm everything else, and the catalog doesn't have enough songs per genre to create real competition.

Any simple tests or comparisons you ran: I ran a before/after weight experiment — doubling the energy weight (1.0 → 2.0) and halving the genre weight (2.0 → 1.0) — then reverted it. For Default Pop/Happy, this flipped the #1 result from Gym Hero to Rooftop Lights, confirming that genre was the deciding factor rather than overall fit. In plain terms: if "Gym Hero" keeps showing up for someone who just wants "Happy Pop," it's because matching genre alone is worth more points than everything else combined — so once a song shares your favorite genre, almost nothing else can catch up to it on the scoreboard, even a song that's a closer match on energy or mood.

---

## 8. Future Work  

If I kept developing this, I'd start by growing the catalog so each genre has multiple songs — right now the genre weight mostly acts as a lookup rather than a real ranking decision, and more density would let energy and mood actually compete for the top spot. I'd also add a diversity constraint to the top-K results (e.g. don't return two songs by the same artist, or cap how many songs from one genre can appear) since right now a small, tightly-clustered set of songs dominates almost every profile. Finally, I'd experiment with incorporating valence as its own scored feature rather than folding it into mood — the two aren't quite the same thing, and testing showed real cases where mood alone missed the emotional tone a song's valence would have caught.

## 9. Personal Reflection  

My biggest learning moment was running the weight-sensitivity experiment in Phase 4 — seeing Gym Hero lose the top spot the instant I rebalanced energy against genre made the abstract idea of "scoring weights shape outcomes" feel concrete instead of theoretical. AI tools helped most with the repetitive parts — writing CSV rows, drafting docstrings, formatting terminal output — but I had to double-check anything involving actual judgment calls, like whether a proposed adversarial profile was genuinely testing something useful or just noise, and whether the bias claims it generated were backed by real evidence from the data rather than a plausible-sounding guess. What surprised me most is how "recommendation-like" a handful of if/else weighted rules can feel — with only four features and simple arithmetic, the system still produces rankings that mostly match my own intuition, which made the filter-bubble risk feel more real: a system this simple can still create the same narrowing effect as a much more sophisticated one, just for more obvious reasons. If I extended this project, I'd want to try a version with real collaborative filtering data (even a tiny simulated "other users liked" signal) just to see how differently the recommendations behave once the system isn't purely comparing a song to itself.
