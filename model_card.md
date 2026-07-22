# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**MusiMatch 1.0**

---

## 2. Intended Use  

MusiMatch takes a person's stated taste (genre, mood, energy, acoustic preference) and picks the top 5 songs from a small catalog that fit best. It assumes the user can honestly describe their taste in those four terms. It's a classroom exploration, not a real product so the catalog is only 18 songs, so it shouldn't be used to actually recommend music to real listeners.

---

## 3. How the Model Works  

Every song gets points added up: 2 points if the genre matches, 2 points if the mood matches, up to 1.5 points for having an energy level close to what the user wants (closer is better, not just "higher"), and 1 point if the song's acousticness matches whether the user likes acoustic music. All the songs get scored this way, then get sorted highest to lowest, and the top 5 are shown with the reasons behind each score.

---

## 4. Data  

18 songs total: the original 10 plus the 8 I added to cover genres and moods that were missing (edm, folk, hip-hop, r&b, metal, classical, country, reggae). Each song has genre, mood, energy, tempo, valence, danceability, and acousticness. It's still a tiny catalog as most genres only have 1-2 songs, and things like lyrics, artist popularity, or actual listening history aren't captured at all.

---

## 5. Strengths  

It works well when a user's genre, mood, and energy all point to the same songs such as "lofi/chill/low energy," which cleanly returned the lofi tracks in order of how close their energy was. Then when comparing "High-Energy Pop" against "Deep Intense Rock", it also swapped the #1 pick exactly as expected, which tells me the genre and mood matching is doing real work, not just defaulting to one favorite song.

---

## 6. Limitations and Bias 

I tested a profile for metal, sad, energy 0.9. The result was that 0 song is tagged both for metal and sad, so the system just used genre + energy and recommended a metal song tagged "angry". The acoustic check also only adds points, never subtracts, so it can't really tell songs apart on that alone. And pop/lofi are the biggest genres in my 18-song catalog, so those profiles get strong lists while rarer genres (classical, reggae) fall back on energy matching alone.

---

## 7. Evaluation  

I ran five profiles through `src/main.py`: default pop/happy, High-Energy Pop, Chill Lofi, Deep Intense Rock, and an adversarial one (`metal/sad/energy=0.9`) meant to test a contradiction.

```
=== Default (pop/happy) ===
User profile: {'genre': 'pop', 'mood': 'happy', 'energy': 0.8}
1. Sunrise City - Score: 5.47 (genre match +2.0, mood match +2.0, energy closeness +1.47)
2. Rooftop Lights - Score: 3.44 (mood match +2.0, energy closeness +1.44)
3. Gym Hero - Score: 3.30 (genre match +2.0, energy closeness +1.30)
4. Concrete Anthem - Score: 1.47 (energy closeness +1.47)
5. Night Drive Loop - Score: 1.42 (energy closeness +1.42)

=== High-Energy Pop ===
User profile: {'genre': 'pop', 'mood': 'happy', 'energy': 0.9, 'acoustic': False}
1. Sunrise City - Score: 6.38 (genre match +2.0, mood match +2.0, energy closeness +1.38, acoustic match +1.0)
2. Gym Hero - Score: 4.46 (genre match +2.0, energy closeness +1.46, acoustic match +1.0)
3. Rooftop Lights - Score: 4.29 (mood match +2.0, energy closeness +1.29, acoustic match +1.0)
4. Storm Runner - Score: 2.48 (energy closeness +1.48, acoustic match +1.0)
5. Neon Static - Score: 2.42 (energy closeness +1.43, acoustic match +1.0)

=== Chill Lofi ===
User profile: {'genre': 'lofi', 'mood': 'chill', 'energy': 0.35, 'acoustic': True}
1. Library Rain - Score: 6.50 (genre match +2.0, mood match +2.0, energy closeness +1.50, acoustic match +1.0)
2. Midnight Coding - Score: 6.39 (genre match +2.0, mood match +2.0, energy closeness +1.40, acoustic match +1.0)
3. Focus Flow - Score: 4.42 (genre match +2.0, energy closeness +1.42, acoustic match +1.0)
4. Spacewalk Thoughts - Score: 4.39 (mood match +2.0, energy closeness +1.40, acoustic match +1.0)
5. Coffee Shop Stories - Score: 2.47 (energy closeness +1.47, acoustic match +1.0)

=== Deep Intense Rock ===
User profile: {'genre': 'rock', 'mood': 'intense', 'energy': 0.9, 'acoustic': False}
1. Storm Runner - Score: 6.48 (genre match +2.0, mood match +2.0, energy closeness +1.48, acoustic match +1.0)
2. Gym Hero - Score: 4.46 (mood match +2.0, energy closeness +1.46, acoustic match +1.0)
3. Neon Static - Score: 2.42 (energy closeness +1.43, acoustic match +1.0)
4. Broken Glass - Score: 2.40 (energy closeness +1.40, acoustic match +1.0)
5. Sunrise City - Score: 2.38 (energy closeness +1.38, acoustic match +1.0)

=== Adversarial (metal / sad / energy=0.9) ===
User profile: {'genre': 'metal', 'mood': 'sad', 'energy': 0.9}
1. Broken Glass - Score: 3.40 (genre match +2.0, energy closeness +1.40)   <- actually tagged "angry," not sad
2. Storm Runner - Score: 1.48 (energy closeness +1.48)
3. Gym Hero - Score: 1.46 (energy closeness +1.46)
4. Neon Static - Score: 1.43 (energy closeness +1.43)
5. Sunrise City - Score: 1.38 (energy closeness +1.38)
```

**Comparisons:**

- **Default vs. High-Energy Pop:** raising the energy target moves Gym Hero (pop, but mood *intense*) up to #2, since its energy is now a closer match. Makes sense.
- **High-Energy Pop vs. Deep Intense Rock:** same energy target, different genre/mood — the #1 pick flips from Sunrise City to Storm Runner as expected, and Gym Hero lands at #2 in both since it's a genuine crossover (pop-tagged, intense mood).
- **Deep Intense Rock vs. Adversarial:** the surprise. Swap "intense" for "sad" and the #1 song barely changes — Broken Glass still wins on genre + energy, even though it's tagged "angry," not sad. The scoring can't tell when a mood mismatch should really matter.

**Plain-language version:** ask for "happy pop" and you might still get "Gym Hero," a pump-up gym anthem, because it's tagged pop and has very high energy — the system can't tell "happy energetic" apart from "aggressive energetic."

**Weight-shift experiment:** I temporarily halved the genre weight and doubled the energy weight, then reran all five profiles. The #1 song barely changed, but #2–#4 shuffled — songs that only matched on mood moved ahead of songs that only matched on genre. A real, explainable shift, but not clearly "more accurate," just a different call on what matters more. Reverted after.

---

## 8. Future Work  

- Add valence and tempo as scoring inputs, not just energy, so "vibe" is captured more fully.
- Capped how many songs from the same artist can show up in one top-5 list, so results feel less repetitive.
- Let a mood mismatch reduce the score instead of just withholding points, so contradictory profiles (like "sad" + "energy 0.9") don't default to whatever matches on genre alone.

---

## 9. Personal Reflection  

The biggest learning moment was the adversarial test as I expected a "sad, high energy" profile to just look weird, but instead it quietly returned an angry metal song as a top pick and looked confident doing it. That's when it clicked that a recommender doesn't know when it's wrong, instead, it just adds up whatever terms happen to match. Using Claude to brainstorm the scoring weights and edge cases sped things up a lot, but I had to actually run the numbers myself to catch things like the acoustic term only ever adding points, never subtracting which wasn't obvious until I saw it in the output. What surprised me most is how convincing a handful of simple weighted rules can feel, which makes it easy to see how real systems with way more data can feel almost magical while still having the same blind spots underneath. If I kept going, I'd want to try weighting valence and tempo in, and see if a small penalty for mood mismatches fixes the metal/sad problem.
