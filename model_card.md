# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

6. Limitations and Bias

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

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
